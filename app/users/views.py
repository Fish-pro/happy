"""
处理与用户相关的路由和视图
"""
import datetime
import json
import math
import os

from flask import request, render_template, redirect, session, make_response

from . import users
from ..models import *

# 手机验证码需要用到下面3个模块
import http.client
from urllib.parse import quote
import random

import json


# 短信验证码接口函数
# 需要传入手机号和验证码
def send_sms(phone, code, APIID='C31546339', APIKEY='2779dc65dde4b950ce5f17379b099a38'):
    # 1. 将中文参数转成url码
    str1 = quote('您的验证码是：', 'utf-8')
    str2 = quote('。请不要把验证码泄露给其他人。', 'utf-8')
    content = '&content=' + str1 + str(code) + str2
    # 2. 将所有参数拼进url
    params = 'account=' + APIID + '&password=' + APIKEY + '&mobile=' + str(phone) + content + '&format=json'
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit&' + params
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # 3. 发送请求
    conn = http.client.HTTPConnection("106.ihuyi.com", port=80, timeout=30)
    # conn.request("POST", sms_send_uri, params, headers)
    conn.request("POST", url, headers=headers)

    # 4. 接收短信是否发送, 发送成功response_str.code == '2'
    response = conn.getresponse()
    response_str = response.read().decode()
    response_str = json.loads(response_str)
    conn.close()
    return response_str


@users.route("/login", methods=["GET", "POST"])
def login_views():
    """
    处理用户的登录请求，严格按照登录流程操作
    :return:
    """
    if request.method == "GET":
        # 获取源地址
        url = request.headers.get('Referer', '/')
        resp = make_response(redirect(url))
        # 将源地址存入cookie
        resp.set_cookie("url", url)
        # 如果session中已经有数据，则直接登录
        if "id" in session and "name" in session:
            return resp
        else:
            # 判断cookie中是否有数据，然后处理
            if "id" in request.cookies and "name" in request.cookies:
                # 取出cookie中的数据进行验证
                id = int(request.cookies["id"])
                name = request.cookies["name"]
                user = Users.query.filter_by(id=id, name=name).first()
                if user:
                    session['id'] = user.id
                    session['name'] = user.name
                    return resp  # 从哪来回哪去
                # 如果cookie中的数据被修改，则清空cookie从新登录
                else:
                    del request.cookies["id"]
                    del request.cookies["name"]
                    return render_template("login.html")
            else:
                return render_template("login.html")

    else:
        # 1.接收提交数据
        phone_num = request.form["phone_num"]
        upwd = request.form["upwd"]
        isActive = "isActive" in request.form
        # 2.验证有效性
        user = Users.query.filter_by(phone=phone_num, password=upwd).first()
        # 3.给出响应
        if user:
            # 1.登录信息保存进session
            session['id'] = user.id
            session['name'] = user.name
            # 2.从cookies中获取源地址(从哪里来回哪里去)
            url = request.cookies.get('url', '/')
            resp = make_response(redirect(url))
            # 3.判断是否保存密码
            if isActive:
                # 4.如果保存密码，存进cookie，存一年
                resp.set_cookie("id", str(user.id), 60 * 60 * 24 * 365)
                resp.set_cookie("name", user.name, 60 * 60 * 24 * 365)
            return resp
        else:
            return render_template("login.html")


@users.route('/register', methods=["GET", "POST"])
def register_views():
    """
    处理登录相关的操作
    :return:
    """
    if request.method == "GET":
        return render_template("register.html")
    else:
        #接收数据并保存进数据库
        user = Users()
        user.name = request.form['uname']
        user.phone = request.form['phone_num']
        user.email = request.form['email']
        user.gender = request.form['gender']
        user.password = request.form['upwd']
        #设置默认头像，如果用户上传头像则修改
        path = "/static/images/headimg/head.gif"
        if "headImg" in request.files:
            f = request.files['headImg']
            ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            fname = ftime + '.' + f.filename.split('.')[-1]
            basedir = os.path.dirname(__file__)
            upload_path = os.path.join(basedir, '../static/images/headimg', fname)
            f.save(upload_path)
            path = "/static/images/headimg/" + fname
        user.head_path = path
        #将数据保存进数据库
        db.session.add(user)
        db.session.commit()
        #将id和name存入session
        session['id'] = user.id
        session['name'] = user.name
        return redirect("/")


@users.route('/reg_phone')
def reg_phone_views():
    """
    处理注册时查询手机号是否被注册
    :return:
    """
    phone = request.args['phone_num']
    reg = Users.query.filter_by(phone=phone).first()
    if reg:
        dic = {"num": 1}  # 手机号已存在
    else:
        dic = {"num": 0}  # 手机号不存在
    jsonStr = json.dumps(dic)
    return jsonStr


@users.route("/check_phone")
def check_phone_views():
    """
    接收用户手机号
    发送短信
    :return: 状态吗和验证码
    """
    phone = request.args["phone_num"]
    #随机生成验证码
    key = random.randint(100000, 999999)
    #发送短信并接受返回值
    check_response = send_sms(phone, key)
    print(check_response)
    # key = 123456
    # check_response = {
    #     "code": 2
    # }
    if check_response["code"] == 2:
        check_response = {
            "code": 2,
            "key": key
        }
    else:
        check_response = {
            "code": 1,
            "key": key
        }
    jsonStr = json.dumps(check_response)
    return jsonStr


# 处理登出
@users.route('/logout')
def logout_views():
    """
    处理登出操作
    :return:
    """
    url = request.headers.get("Referer", "/")
    if "id" in session and "name" in session:
        del session["id"]
        del session["name"]
    return redirect(url)


@users.route("/becomeFan")
def becomeFan_views():
    """
    处理用户关注
    :return:
    """
    if "id" in session and "name" in session:
        #接收被关注的用户的id并和用户id一起存入数据库
        id = session["id"]
        star_id = request.args["star_id"]
        #判断是否已经关注过，如果有则提醒前端，如果没有则存入数据库并返回状态码
        conn = User_attention.query.filter_by(user_fan_id=id, user_star_id=star_id).first()
        if conn:
            res = {"num": 2}
        else:
            user_attention = User_attention()
            user_attention.user_fan_id = id
            user_attention.user_star_id = star_id
            db.session.add(user_attention)
            res = {"num": 1}
    else:
        #没在登录状态，提醒用户登录后才能关注
        res = {"num": 0}
    jsonStr = json.dumps(res)
    return jsonStr


@users.route('/find_upwd', methods=["GET", "POST"])
def find_upwd_views():
    """
    处理用户找回密码的操作
    :return:
    """
    if request.method == "GET":
        return render_template("find_upwd.html")
    else:
        phone = request.form["phone_num"]
        user = Users.query.filter_by(phone=phone).first()
        user.password = request.form["upwd"]
        db.session.add(user)
        return redirect("/")


@users.route("/change_file", methods=["GET", "POST"])
def change_file_views():
    """
    处理用户修改资料的操作
    :return:
    """
    #如果能进入修改资料页面，该用户一定在登录状态
    id = session['id']
    if request.method == "GET":
        user = Users.query.filter_by(id=id).first()
        fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
        idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)

        #将用户的所有的粉丝存入列表
        l1 = []
        for i in fans.all():
            l1.append(Users.query.filter_by(id=i[0]).first())
        #将用户的所有的关注对象存入列表
        l2 = []
        for j in idos.all():
            l2.append(Users.query.filter_by(id=j[0]).first())
        return render_template("change_file.html", params=locals())
    else:
        user = Users.query.filter_by(id=id).first()
        if "headImg" in request.files:
            f = request.files['headImg']
            ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            fname = ftime + '.' + f.filename.split('.')[-1]
            basedir = os.path.dirname(__file__)
            upload_path = os.path.join(basedir, '../static/images/headimg', fname)
            f.save(upload_path)
            path = "/static/images/headimg/" + fname
            user.head_path = path
        if "uname" in request.form:
            user.name = request.form["uname"]
        if "email" in request.form:
            user.email = request.form["email"]
        if "upwd" in request.form:
            user.password = request.form["upwd"]
        db.session.add(user)
        return redirect("/myspace?note_info=my")


@users.route('/friend_list')
def friend_list_views():
    """
    处理好友列表的显示操作
    :return:
    """
    if "id" in session and "name" in session:
        id = session['id']
        user = Users.query.filter_by(id=id).first()
        fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
        idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)

        #l1用于存储用户的粉丝
        l1 = []
        #l3用于存储与用户相互关注的用户
        l3 = []
        for i in fans.all():
            if i in idos.all():
                l3.append(Users.query.filter_by(id=i[0]).first())
            else:
                l1.append(Users.query.filter_by(id=i[0]).first())
        #l2用于存储用户关注的对象
        l2 = []
        for j in idos.all():
            if j not in fans.all():
                l2.append(Users.query.filter_by(id=j[0]).first())

        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:6]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:6]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]

        return render_template("friend_list.html", params=locals())
    else:
        return redirect("/login")


@users.route("/cancel_fan")
def cancel_fan_views():
    """
    处理取关操作
    :return:
    """
    star_id = request.args["star_id"]
    fan_id = session["id"]
    star_fan = User_attention.query.filter_by(user_fan_id=fan_id, user_star_id=star_id).first()
    if star_fan:
        db.session.delete(star_fan)
    return redirect("/friend_list")


@users.route("/become_fan")
def become_fan_views():
    """
    处理用户的关注操作
    :return:
    """
    star_id = request.args["user_id"]
    fan_id = session["id"]
    star_fan = User_attention()
    star_fan.user_fan_id = fan_id
    star_fan.user_star_id = star_id
    db.session.add(star_fan)
    return redirect("/friend_list")


@users.route('/person')
def person_list_views():
    """
    处理用户个人中心的显示操作
    :return:
    """
    if "id" in session and "name" in session:
        user_id = request.args["user_id"]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:6]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:6]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]

        user1 = Users.query.filter_by(id=user_id).first()
        fans1 = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == user_id)
        idos1 = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == user_id)

        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
            fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
            idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
            l2 = []
            for j in idos.all():
                l2.append(j[0])
        # 每页显示的记录数量
        pageSize = 15
        # 接收前段传过来的参数page,,如果没有传递过来，则默认为１，并保存在page变量中
        page = int(request.args.get('page', 1))
        ost = (page - 1) * pageSize
        if "choosePage" in request.args:
            choosePage = int(request.args["choosePage"])
            ost = (choosePage - 1) * pageSize
            page = choosePage

        # notes = db.session.query(Notes).offset(ost).limit(pageSize).all()
        notes = Notes.query.filter_by(user_id=user_id).all()[::-1]
        # 根据pageSize计算尾页
        totalCount = len(notes)
        lastPage = math.ceil(totalCount / pageSize)
        notes = notes[ost:(ost + pageSize)]
        # 计算上一页
        prePage = page - 1
        if prePage < 1:
            prePage = 1
        # 计算下一页
        nextPage = lastPage
        if page < lastPage:
            nextPage = page + 1

        return render_template("info.html", params=locals())
    else:
        return redirect("/login")


@users.route('/adminlogin', methods=["GET", "POST"])
def adminlogin_views():
    """
    处理管理员的登录操作
    :return:
    """
    if request.method == "GET":
        if "admin" in session:
            return redirect("/admin")
        else:
            return render_template("adminlogin.html")
    else:
        adminname = request.form["adminname"]
        upwd = request.form["upwd"]
        print(adminname)
        print(upwd)
        admin = Admins.query.filter_by(admin_name=adminname, admin_pwd=upwd).first()
        if admin:
            session["admin"] = adminname
            return redirect("/admin")
        else:
            return redirect("/adminlogin")


@users.route("/admin")
def admin_views():
    """
    用于显示管理员主页面
    :return:
    """
    if "admin" in session:
        admin_name = session["admin"]
        admin = Admins.query.filter_by(admin_name=admin_name).first()
        users = Users.query.all()
        man = 0
        woman = 0
        for u in users:
            if u.gender == 1:
                man += 1
            else:
                woman += 1
        total_users = Users.query.count()
        total_notes = Notes.query.count()
        notes = Notes.query.all()[::-1]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()
        total_words = db.session.query(Note_content).filter(Note_content.type == 1).count()

        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()
        total_pictures = db.session.query(Note_content).filter(Note_content.type == 2).count()

        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()
        total_gifs = db.session.query(Note_content).filter(Note_content.type == 3).count()

        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()
        total_videos = db.session.query(Note_content).filter(Note_content.type == 4).count()

        pageSize = 15
        # 接收前段传过来的参数page,,如果没有传递过来，则默认为１，并保存在page变量中
        page = int(request.args.get('page', 1))
        ost = (page - 1) * pageSize
        if "choosePage" in request.args:
            choosePage = int(request.args["choosePage"])
            ost = (choosePage - 1) * pageSize
            page = choosePage
        # notes = db.session.query(Notes).offset(ost).limit(pageSize).all()
        notes = notes[ost:(ost + pageSize)]
        # 根据pageSize计算尾页
        totalCount = db.session.query(Notes).count()
        lastPage = math.ceil(totalCount / pageSize)
        # 计算上一页
        prePage = page - 1
        if prePage < 1:
            prePage = 1
        # 计算下一页
        nextPage = lastPage
        if page < lastPage:
            nextPage = page + 1
        return render_template("admin_index.html", params=locals())
    else:
        return redirect("/adminlogin")


# 处理管理员登出
@users.route('/adminlogout')
def adminlogout_views():
    if "admin" in session:
        del session["admin"]
    return redirect("/adminlogin")
