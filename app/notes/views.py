"""
只处理与帖子相关的路由和视图
"""
import datetime
import os

from flask import render_template, request, session, redirect

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


# 分享段子
@notes.route("/add_word", methods=["GET", "POST"])
def add_word_views():
    # 用session中的phone获得用户对象
    if request.method == "GET":
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
        return render_template("add_word.html", params=locals())
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
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
        return render_template("add_picture.html", params=locals())
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
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
        return render_template("add_gif.html", params=locals())
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
        if "id" in session and "name" in session:
            id = session['id']
            user = Users.query.filter_by(id=id).first()
        return render_template("add_video.html", params=locals())
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
    type = int(request.args['type'])
    contents = Note_content.query.filter_by(type=type).all()
    notes = []
    for con in contents:
        notes.append(con.note)
    if "id" in session and "name" in session:
        id = session['id']
        user = Users.query.filter_by(id=id).first()
    return render_template("index.html", params=locals())
