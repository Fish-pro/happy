"""
处理与用户相关的路由和视图
"""
import datetime
import os

from flask import request, render_template, redirect, session, make_response

from . import users
from ..models import *


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
            return render_template("login.html")


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


@users.route('/register_phone')
def register_phone_views():
    phone = request.args['phone_num']
    reg = Users.query.filter_by(phone=phone).first()
    print(reg)
    if reg:
        return '1'  # 手机号已存在
    else:
        return '0'  # 手机号不存在


# 处理登出
@users.route('/logout')
def logout_views():
    url = request.headers.get("Referer", "/")
    if "id" in session and "name" in session:
        del session["id"]
        del session["name"]
    return redirect(url)
