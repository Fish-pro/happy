"""
只处理与帖子相关的路由和视图
"""
import datetime
import math
import os
import json

from flask import render_template, request, session, redirect

from app.main.views import sort_notes
from . import notes
from .. import db
from ..models import *

# 定义一个函数用于图片动图，视频文件的存储并返回保存路劲
def saveFile(f, path):
    # 2.构建保存路劲
    ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    ext = f.filename.split('.')[-1]
    filename = ftime + '.' + ext
    basedir = os.path.dirname(__file__)
    upload_path = os.path.join(basedir, "../static/images", path, filename)
    path = "../static/images/" + path + "/" + filename
    # 3.保存文件到相应目录处
    f.save(upload_path)
    return path


def sort_notes(x):
    return x.notes.count()

# 分享段子
@notes.route("/add_word", methods=["GET", "POST"])
def add_word_views():
    # 用session中的phone获得用户对象
    if request.method == "GET":
        # 读取所有用户信息
        users = Users.query.all()
        users = sorted(users, key=sort_notes, reverse=True)[0:6]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]
        # 判断是否有登录用户(id和name)
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
            fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
            idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
            l2 = []
            for j in idos.all():
                l2.append(j[0])
            return render_template("add_word.html", params=locals())
        else:
            return render_template("login.html")
    else:
        # 接受数据
        uid = request.form['uid']
        type = request.form['type']
        title = request.form['title']
        wordContent = request.form['wordContent']
        # 将数据存入notes和note_content表
        note_content = Note_content()
        note_content.title = title
        note_content.content = wordContent
        note_content.type = int(type)

        note = Notes()
        note.user_id = uid
        create_date = datetime.datetime.now()
        note.create_date = create_date
        note.note_raise = 0
        note.down = 0
        note.content = note_content
        # 提交数据到数据库
        db.session.add(note)
        return redirect("/")


# 分享图片
@notes.route("/add_picture", methods=["GET", "POST"])
def add_picture_views():
    if request.method == "GET":
        # 读取所有用户信息
        users = Users.query.all()
        users = sorted(users, key=sort_notes, reverse=True)[0:6]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]
        # 判断是否有登录用户(id和name)
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
            fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
            idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
            l2 = []
            for j in idos.all():
                l2.append(j[0])
            return render_template("add_picture.html", params=locals())
        else:
            return render_template("login.html")
    else:
        uid = request.form['uid']
        type = request.form['type']
        title = request.form['title']
        path = ""  # 请求错时默认文件路径
        if 'picture' in request.files:
            f = request.files['picture']
            path = saveFile(f, "picture")
        # 将数据存入notes和note_content表
        note_content = Note_content()
        note_content.title = title
        note_content.content = path
        note_content.type = int(type)

        note = Notes()
        note.user_id = uid
        create_date = datetime.datetime.now()
        note.create_date = create_date
        note.note_raise = 0
        note.down = 0
        note.content = note_content
        # 提交数据到数据库
        db.session.add(note)
        return redirect("/")


# 分享动图
@notes.route("/add_gif", methods=["GET", "POST"])
def add_gif_views():
    if request.method == "GET":
        # 读取所有用户信息
        users = Users.query.all()
        users = sorted(users, key=sort_notes, reverse=True)[0:6]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]
        # 判断是否有登录用户(id和name)
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
            fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
            idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
            l2 = []
            for j in idos.all():
                l2.append(j[0])
            return render_template("add_gif.html", params=locals())
        else:
            return render_template("login.html")
    else:
        uid = request.form['uid']
        type = request.form['type']
        title = request.form['title']
        path = ""  # 请求错时默认文件路径
        if 'picture' in request.files:
            f = request.files['picture']
            path = saveFile(f, "gif")
        # 将数据存入notes和note_content表
        note_content = Note_content()
        note_content.title = title
        note_content.content = path
        note_content.type = int(type)

        note = Notes()
        note.user_id = uid
        create_date = datetime.datetime.now()
        note.create_date = create_date
        note.note_raise = 0
        note.down = 0
        note.content = note_content
        # 提交数据到数据库
        db.session.add(note)
        return redirect("/")


# 分享视频
@notes.route("/add_video", methods=["GET", "POST"])
def add_video_views():
    if request.method == "GET":
        # 读取所有用户信息
        users = Users.query.all()
        users = sorted(users, key=sort_notes, reverse=True)[0:6]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]
        # 判断是否有登录用户(id和name)
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
            fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
            idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
            l2 = []
            for j in idos.all():
                l2.append(j[0])
            return render_template("add_video.html", params=locals())
        else:
            return render_template("login.html")
    else:
        uid = request.form['uid']
        type = request.form['type']
        title = request.form['title']
        path = ""  # 请求错时默认文件路径
        if 'picture' in request.files:
            f = request.files['picture']
            path = saveFile(f, "video")
        # 将数据存入notes和note_content表
        note_content = Note_content()
        note_content.title = title
        note_content.content = path
        note_content.type = int(type)

        note = Notes()
        note.user_id = uid
        create_date = datetime.datetime.now()
        note.create_date = create_date
        note.note_raise = 0
        note.down = 0
        note.content = note_content
        # 提交数据到数据库
        db.session.add(note)
        return redirect("/")


# 处理永久导航分类栏
@notes.route("/longclass")
def longclass_views():
    # 读取所有用户信息
    users = Users.query.all()
    users = sorted(users, key=sort_notes, reverse=True)[0:6]
    words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
    pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
    gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
    videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]
    # 判断是否有登录用户(id和name)
    if "id" in session and "name" in session:
        id = session['id']
        user = Users.query.filter_by(id=id).first()
        fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
        idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
        l2 = []
        for j in idos.all():
            l2.append(j[0])
    # 每页显示的记录数量
    pageSize = 20
    # 接收前段传过来的参数page,,如果没有传递过来，则默认为１，并保存在page变量中
    page = int(request.args.get('page', 1))
    ost = (page - 1) * pageSize
    if "choosePage" in request.args:
        choosePage = int(request.args["choosePage"])
        ost = (choosePage - 1) * pageSize
        page = choosePage

    type = int(request.args['type'])
    contents = Note_content.query.filter_by(type=type).all()
    notes = []
    for con in contents:
        notes.append(con.note)
    notes = notes[::-1]

    notes = notes[ost:(ost + pageSize)]
    # 根据pageSize计算尾页
    totalCount = Note_content.query.filter_by(type=type).count()
    lastPage = math.ceil(totalCount / pageSize)
    # 计算上一页
    prePage = page - 1
    if prePage < 1:
        prePage = 1
    # 计算下一页
    nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1

    return render_template("longclass.html", params=locals())


@notes.route("/comment")
def comment_views():
    if "id" in session and "name" in session:
        id = session["id"]
        user = Users.query.filter_by(id=id).first()
        note_id = request.args["note_id"]
        text = request.args["text"]
        comment = Note_comment()
        comment.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment.content = text
        comment.note_id = note_id
        comment.user_id = user.id
        comment.comment_raise = 0
        comment.down = 0
        db.session.add(comment)

        comments = Note_comment.query.all()
        print(comment)
        l = []
        for com in comments:
            if com.note_id == note_id:
                l.append(com.to_dict())
        l = l[::-1]
        jsonStr = json.dumps(l)
        print(jsonStr)
        return jsonStr
    else:
        return redirect("/login")


@notes.route("/like")
def like_views():
    note_id = request.args["note_id"]
    note = Notes.query.filter_by(id=note_id).first()
    note.note_raise += 1
    db.session.add(note)
    dict = {"raise": note.note_raise}
    jsonStr = json.dumps(dict)
    return jsonStr


@notes.route("/unlike")
def unlike_views():
    note_id = request.args["note_id"]
    note = Notes.query.filter_by(id=note_id).first()
    note.down += 1
    db.session.add(note)
    dict = {"down": note.down}
    jsonStr = json.dumps(dict)
    return jsonStr


@notes.route("/com_like")
def com_like_views():
    com_id = request.args["com_id"]
    comment = Note_comment.query.filter_by(id=com_id).first()
    comment.comment_raise += 1
    db.session.add(comment)
    dict = {"raise": comment.comment_raise}
    jsonStr = json.dumps(dict)
    return jsonStr


@notes.route("/com_unlike")
def com_unlike_views():
    com_id = request.args["com_id"]
    print(com_id)
    comment = Note_comment.query.filter_by(id=com_id).first()
    comment.down += 1
    db.session.add(comment)
    dict = {"down": comment.down}
    jsonStr = json.dumps(dict)
    return jsonStr


@notes.route("/addbook")
def addbook_views():
    try:
        note_id = request.args["note_id"]

        id = session["id"]
        attention1 = User_note_attention.query.filter_by(user_id=id, note_id=note_id).first()
        if attention1:
            res = {"num":2}
        else:
            attention = User_note_attention()
            attention.note_id = note_id
            attention.user_id = id
            db.session.add(attention)
            res = {"num": 1}
    except:
        res = {"num": 0}
    jsonStr = json.dumps(res)
    return jsonStr
