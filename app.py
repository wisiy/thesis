from datetime import timedelta
from functools import wraps
from flask import Flask, render_template, redirect, request, url_for, flash, session
from sqlalchemy import or_
import pandas as pd
import numpy as np
import config
import os
from models import db, User, Studentinfo, Major, Province, Log
from flask import send_from_directory

app = Flask(__name__, static_url_path='')
app.config.from_object(config)
db.init_app(app)

app.jinja_env.variable_start_string = '{{ '
app.jinja_env.variable_end_string = ' }}'


def checking_login(f):
    """
    登录装饰器，验证登录 @checking_login
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/index/')
def hello_world():
    return "<script>alert('Hello You Guys!');location.href='/';</script>"


@app.route('/')
def index():
    """
    主页
    """
    total_user = User.query.count()
    record = Studentinfo.query.count()
    return render_template('index.html', record=record, total_user=total_user)


@app.route('/login/', methods=["GET", "POST"])
def login():
    """
    登录
    """
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 获取登录表单数据
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        # print(username, password, user.username, user.password)
        if user is None:
            flash('该用户名不存在！')
            return redirect(url_for('login'))
        elif user.username == username and user.password == password:
            # 记录部分用户个人数据到session
            session['username'] = user.username
            session['name'] = user.name
            session['is_admin'] = user.is_admin
            session['add_time'] = user.add_time
            # session['user'] = user
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=60)  # session存活时间
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误！')
            return redirect(url_for('login'))


@app.route('/reset/password/', methods=['GET', 'POST'])
def reset_password():
    """
    修改密码
    :return:
    """
    if request.method == 'GET':
        return render_template("reset_password.html")
    else:
        ori_pass = request.form.get("initial-password")
        new_pass = request.form.get("password")
        confirm = request.form.get("confirm")
        user = User.query.filter_by(username=session["username"]).first()
        if ori_pass != user.password:
            flash('原密码不正确！')
            return redirect(url_for("reset_password"))
        elif new_pass != confirm:
            flash('两次输入的密码不一致')
            return redirect(url_for("reset_password"))
        elif new_pass == ori_pass:
            flash('新旧密码不能一样')
            return redirect(url_for("reset_password"))
        else:
            user.password = new_pass
            db.session.add(user)
            db.session.commit()
            session.clear()
            return "<script>alert('密码修改成功');location.href='/login/';</script>"


@app.route('/quit/')
def sign_out():
    """
    退出
    """
    session.clear()  # 清除session
    return redirect(url_for("login"))


@app.route("/new/user/", methods=['GET', 'POST'])
def new_user():
    """
    添加用户
    """
    if request.method == 'GET':
        return render_template('new_user.html')
    else:
        # 新增用户获取表单数据
        username = request.form.get('username')
        name = request.form.get('name')
        phone = request.form.get('phone')
        password = request.form.get('password')
        password_sure = request.form.get('confirm')
        is_admin = request.form.get('is_admin')
        # 如果用户名被用了，就不能注册
        user = User.query.filter(User.username == username).first()
        # admin = Admin.query.filter(Admin.username == username).first()
        if user:
            flash('该用户名已存在')
            return redirect(url_for('new_user'))
        else:
            # 检查两次输入的密码是否相等
            if password != password_sure:
                flash('两次密码输入不一致！')
                return redirect(url_for('new_user'))
            else:
                # 写入数据库，数据库字段名=表单列名
                user = User(username=username, password=password, phone=phone, name=name, is_admin=is_admin)
                db.session.add(user)
                db.session.commit()
                return "<script>alert('添加成功！');location.href='';</script>"


@app.route('/user/list/')
def user_list():
    """
    用户列表
    """
    users = User.query.order_by(User.id.desc()).all()
    return render_template('user_list.html', users=users)


@app.route('/user/detail/<int:uid>', methods=['GET', 'POST'])
def user_detail(uid=None):
    """
    获取用户的详细信息
    :param uid: user id
    """
    user = User.query.get_or_404(int(uid))
    return render_template("detail_user.html", user=user)


@app.route('/user/del/<int:udid>')
def user_del(udid=None):
    """
    删除用户
    :param udid: user delete id
    """
    user = User.query.get_or_404(udid)
    db.session.delete(user)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('user_list'))


@app.route('/major/list/')
def major():
    """
    专业列表
    """
    major_list = Major.query.order_by(Major.code_major.asc()).all()
    return render_template('major.html', major_list=major_list)


@app.route('/delete/major/<int:mid>', methods=['GET'])
def del_major(mid=None):
    """
    删除专业
    :param mid: major id
    """
    major_del = Major.query.get_or_404(mid)
    db.session.delete(major_del)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for("major"))


@app.route('/student/all/')
def student_all():
    """
    所有学生
    """
    students = Studentinfo.query.order_by(Studentinfo.final_score.asc()).all()
    return render_template('all_student.html', students=students)


@app.route('/student/detail/<int:sid>', methods=['GET', 'POST'])
def student_detail(sid=None):
    """
    表格：
    :param sid: student id
    :return: 重载 reload刷新学生的详细信息
    """
    student_info = Studentinfo.query.get_or_404(int(sid))   # 通过id去获取学生的详细信息
    major_info = Major.query.order_by(Major.code_major.asc()).all()  # 获取专业列表
    province_info = Province.query.order_by(Province.code.asc()).all()  # 获取省份列表
    if request.method == 'GET':
        return render_template("detail_student.html", si=student_info, mi=major_info, pi=province_info)
    else:
        # 如果有更改，则将更改后的数据提交至数据库，再返回到页面
        student_info.examinee_number = request.form.get('examinee_number')
        student_info.name = request.form.get('name')
        student_info.registration_number = request.form.get('registration_number')
        student_info.international = request.form.get('international')
        # 通过切片获取出生年月
        id_number = request.form.get('id_number')
        student_info.id_number = id_number
        student_info.birthday = id_number[6:10]+'年'+id_number[10:12]+'月'+id_number[12:14]+'日'
        # print(student_info.birthday)
        student_info.sex = request.form.get('sex')
        student_info.height = request.form.get('height')
        student_info.high_school = request.form.get('high_school')
        student_info.major = request.form.get('major')
        student_info.major_direction = request.form.get('major_direction')
        student_info.view_package = request.form.get('view_package')
        student_info.test_package = request.form.get('test_package')
        student_info.view_score = request.form.get('view_score')
        student_info.test_score = request.form.get('test_score')
        student_info.final_score = request.form.get('final_score')
        # print(request.form.get('final_score'))
        student_info.afford_fee = request.form.get('afford_fee')
        student_info.art_science = request.form.get('art_science')
        student_info.household_type = request.form.get('household_type')
        student_info.phone_1 = request.form.get('phone_1')
        student_info.phone_2 = request.form.get('phone_2')
        student_info.province = request.form.get('province')
        student_info.recipient = request.form.get('recipient')
        student_info.note = request.form.get('note')
        student_info.post_address = request.form.get('post_address')
        # print(request.form.get('afford_fee'), request.form.get('art_science'))
        db.session.add(student_info)
        db.session.commit()
        # print(student_info.add_time)
        return "<script>location.href='';</script>"


@app.route('/results/list/')
def results_list():
    """
    查找出来的学生列表，返回值是一个列表
    """
    keywords = request.args.get('keywords', type=str)
    # 通过身份证号、考生号、报考号、姓名、以及id来寻找所有符合条件的学生信息
    data = Studentinfo.query.filter(or_(Studentinfo.id_number.like("%" + keywords + "%"),
                                        Studentinfo.examinee_number.like("%" + keywords + "%"),
                                        Studentinfo.registration_number.like("%" + keywords + "%"),
                                        Studentinfo.name.like("%" + keywords + "%"),
                                        Studentinfo.id.like("%" + keywords + "%"))
                                    ).order_by(Studentinfo.add_time.desc()).all()
    # 如果没有符合条件的考生，返回一个提示
    if not data:
        return "<script>alert('没有符合该信息的学生');location.href='/';</script>"
    else:
        return render_template('result_list.html', data=data)   # 返回一个数据列表


@app.route('/import/excel/', methods=['GET', 'POST'])
def excel_import():
    if request.method == 'GET':
        return render_template("excel_import.html")
    else:
        file = request.files['file-upload']
        filename = file.filename
        print(filename, type(file))
        read = pd.read_excel(file)
        # res = read.head()
        data = read.iloc[:].values
        print(data)  # 格式化输出
        return render_template("excel_import.html", data=data)


@app.errorhandler(404)
def page_not_found(error):
    """
    访问到未注册的页面时返回404
    :param error: 404
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
