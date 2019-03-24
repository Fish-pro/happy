"""
处理与用户相关的路由和视图
"""
import datetime
import json
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
def send_sms(phone, code, APIID='C66978111', APIKEY='5698d0d7f9f7eab406e92828c3a373b0'):
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
    if request.method == "GET":
        url = request.headers.get('Referer', '/')
        resp = make_response(redirect(url))
        resp.set_cookie("url", url)
        if "id" in session and "name" in session:
            return resp
        else:
            if "id" in request.cookies and "name" in request.cookies:
                id = int(request.cookies["id"])
                name = request.cookies["name"]
                user = Users.query.filter_by(id=id, name=name).first()
                if user:
                    session['id'] = user.id
                    session['name'] = user.name
                    return resp  # 从哪来回哪去
                else:
                    del request.cookies["id"]
                    del request.cookies["name"]
                    return render_template("login.html")
            else:
                return render_template("login.html")

        # resp = make_response(render_template("login.html"))
        # # 获取源地址，将地址保存进cookies
        # url = request.headers.get('Referer', '/')
        # resp.set_cookie("url", url)
        # return resp
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
            if isActive:
                resp.set_cookie("id", str(user.id))
                resp.set_cookie("name", user.name)
            return resp
        else:
            return "用户或密码不正确，你可以<a href='/login'>重新登录</a>"


@users.route('/register', methods=["GET", "POST"])
def register_views():
    if request.method == "GET":
        url = request.headers.get('Referer', '/')
        resp = make_response(render_template("register.html"))
        resp.set_cookie("url", url)
        return resp
    else:
        user = Users()
        user.name = request.form['uname']
        user.phone = request.form['phone_num']
        user.email = request.form['email']
        user.gender = request.form['gender']
        user.password = request.form['upwd']
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

        db.session.add(user)
        db.session.commit()
        # user = Users.query.filter_by(phone=user.phone).first()
        session['id'] = user.id
        session['name'] = user.name
        url = request.cookies.get('url', '/')
        return redirect(url)


@users.route('/reg_phone')
def reg_phone_views():
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
    phone = request.args["phone_num"]
    key = random.randint(100000, 999999)
    check_response = send_sms(phone, key)
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
    url = request.headers.get("Referer", "/")
    if "id" in session and "name" in session:
        del session["id"]
        del session["name"]
    return redirect(url)


@users.route("/becomeFan")
def becomeFan_views():
    if "id" in session and "name" in session:
        id = session["id"]
        star_id = request.args["star_id"]
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
        res = {"num": 0}
    jsonStr = json.dumps(res)
    return jsonStr
