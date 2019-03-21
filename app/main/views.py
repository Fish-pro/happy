"""
只处理与主题相关的路由和视图
"""
from flask import render_template, request, session

from . import main
from .. import db
from ..models import *


def sort_notes(x):
    return x.notes.count()


@main.route('/')
def index_views():
    # 读取表中所有的内容
    notes = Notes.query.all()[::-1]
    # 读取所有用户信息
    users = Users.query.all()
    users = sorted(users, key=sort_notes, reverse=True)[0:6]
    words = db.session.query(Note_content).filter(Note_content.type==1).all()[:6]
    pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
    gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
    videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]
    # 判断是否有登录用户(id和name)
    if "id" in session and "name" in session:
        id = session['id']
        user = Users.query.filter_by(id=id).first()
    return render_template("index.html", params=locals())


@main.route('/list')
def list_views():
    return render_template("list.html")


@main.route('/class')
def class_views():
    return render_template("class.html")


@main.route('/friends')
def friends_views():
    return render_template("friends.html")


@main.route('/myspace')
def myspace_views():
    return render_template("myspace.html")
