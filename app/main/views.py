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


def sort_raise(x):
    return x.note_raise


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
    pageSize = 15
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
    notes = sorted(notes, key=sort_raise, reverse=True)

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

    return render_template("list.html", params=locals())


@main.route('/class')
def class_views():
    if "id" in session and "name" in session:
        id = session["id"]
        user = Users.query.filter_by(id=id).first()
    return render_template("class.html", params=locals())


@main.route("/search")
def search_views():
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

    key = request.args["key"]
    contents = db.session.query(Note_content).filter(Note_content.title.like('%' + key + '%')).all()
    notes = []
    for con in contents:
        notes.append(con.note)
    notes = notes[::-1]

    # 每页显示的记录数量
    pageSize = 15
    # 接收前段传过来的参数page,,如果没有传递过来，则默认为１，并保存在page变量中
    page = int(request.args.get('page', 1))
    ost = (page - 1) * pageSize
    if "choosePage" in request.args:
        choosePage = int(request.args["choosePage"])
        ost = (choosePage - 1) * pageSize
        page = choosePage

    notes = notes[ost:(ost + pageSize)]
    # 根据pageSize计算尾页
    totalCount = len(notes)
    flag = False
    if totalCount > 0:
        flag = True
    lastPage = math.ceil(totalCount / pageSize)
    # 计算上一页
    prePage = page - 1
    if prePage < 1:
        prePage = 1
    # 计算下一页
    nextPage = lastPage
    if page < lastPage:
        nextPage = page + 1

    return render_template('serach.html', params=locals())


@main.route('/friends')
def friends_views():
    if "id" in session and "name" in session:
        # 读取所有用户信息
        users = Users.query.all()
        users = sorted(users, key=sort_notes, reverse=True)[0:6]
        words = db.session.query(Note_content).filter(Note_content.type == 1).all()[:6]
        pictures = db.session.query(Note_content).filter(Note_content.type == 2).all()[:4]
        gifs = db.session.query(Note_content).filter(Note_content.type == 3).all()[:4]
        videos = db.session.query(Note_content).filter(Note_content.type == 4).all()[:6]

        id = session['id']
        user = Users.query.filter_by(id=id).first()
        fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
        idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)
        l2 = []
        for j in idos.all():
            l2.append(j[0])

        note_info = request.args["note_info"]
        notes = []
        if note_info == "粉丝":
            for fan in fans.all():
                notes.extend(Notes.query.filter_by(user_id=fan.user_fan_id).all())
                print(notes)
        if note_info == "关注":
            for ido in idos.all():
                notes.extend(Notes.query.filter_by(user_id=ido.user_star_id).all())
                print(notes)
        notes = notes[::-1]
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

        return render_template("friends.html", params=locals())
    else:
        return render_template("login.html")


@main.route('/myspace')
def myspace_views():
    if "id" in session and "name" in session:
        id = session['id']
        user = Users.query.filter_by(id=id).first()
        fans = db.session.query(User_attention.user_fan_id).filter(User_attention.user_star_id == id)
        idos = db.session.query(User_attention.user_star_id).filter(User_attention.user_fan_id == id)

        l1 = []
        for i in fans.all():
            l1.append(Users.query.filter_by(id=i[0]).first())

        l2 = []
        for j in idos.all():
            l2.append(Users.query.filter_by(id=j[0]).first())

        note_info = request.args["note_info"]
        notes = []
        if note_info == "my":
            notes = Notes.query.filter_by(user_id=id).all()
        if note_info == "addblog":
            user_note = User_note_attention.query.filter_by(user_id = id).all()
            for un in user_note:
                notes.append(Notes.query.filter_by(id=un.note_id).first())
        notes = notes[::-1]
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

        return render_template("myspace.html", params=locals())
    else:
        return render_template("login.html")


@main.route("/info")
def info_views():
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
    note_id = request.args["note_id"]
    note = Notes.query.filter_by(id=note_id).first()
    if int(note_id) > 1:
        prev_note_id = int(note_id) - 1
    else:
        prev_note_id = 1
    if int(note_id) < Notes.query.count():
        next_note_id = int(note_id) + 1
    else:
        next_note_id = Notes.query.count()

    return render_template("read.html", params=locals())
