"""
只处理与主题相关的路由和视图
"""
import math

from flask import render_template, request, session

from . import main
from .. import db
from ..models import *


def sort_notes(x):
    return x.notes.count()


@main.route('/')
def index_views():
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
        fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id==id)
        idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id==id)
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
    # notes = db.session.query(Notes).offset(ost).limit(pageSize).all()
    notes = Notes.query.all()[::-1]
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
