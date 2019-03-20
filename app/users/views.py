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
            url = request.cookies.get('url')
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
        return render_template("register.html")
    else:
        # 接受数据
        uname = request.form["uname"]
        phone_num = request.form["phone_num"]
        email = request.form["email"]
        gender = request.form["gender"]
        upwd = request.form["upwd"]

        if 'headImg' in request.files:
            # 1.获取文件
            f = request.files['headImg']
            # 2.构建保存路劲
            ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            ext = f.filename.split('.')[-1]
            filename = ftime + '.' + ext
            basedir = os.path.dirname(__file__)
            upload_path = os.path.join(basedir, "static/headimg/", filename)
            path = "/static/headimg/" + filename
            # 3.保存文件到相应目录处
            f.save(upload_path)
        else:
            path = "/static/headimg/head.gif"
        user = Users()
        user.name = uname
        user.phone = phone_num
        user.email = email
        user.gender = gender
        user.password = upload_path
        user.head_path = path
        db.session.add(user)
        url_referer = request.headers.get('Referer')
        return redirect(url_referer)


# 处理登出
@users.route('/logout')
def logout_views():
    url = request.headers.get("Referer", "/")
    if "id" in session and "name" in session:
        del session["id"]
        del session["name"]
    return redirect(url)
