from . import db

# 1.管理员信息表
class Admins(db.Model):
    __teblename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(30), nullable=False)
    admin_pwd = db.Column(db.String(20), nullable=False)


# 2.用户基本信息表
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(18), nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(30), nullable=True)
    gender = db.Column(db.Integer, nullable=False)
    head_path = db.Column(db.String(100), nullable=True)
    # 用户发送的帖子(与notes一对多)
    notes = db.relationship("Notes", backref='user', lazy='dynamic')
    # 用户关注的帖子，与user_note_attention表建立一对多关系
    attentions = db.relationship("User_note_attention", backref='user', lazy='dynamic')
    # 与note_comment建立一对多关系
    user_comments = db.relationship("Note_comment", backref='user', lazy='dynamic')


# 3.用户/用户关注表
class User_attention(db.Model):
    __tablename__ = 'user_attention'
    user_attention_id = db.Column(db.Integer, primary_key=True)
    user_fan_id = db.Column(db.Integer, nullable=False)
    user_star_id = db.Column(db.Integer, nullable=False)


# 4.用户/帖子关注表
class User_note_attention(db.Model):
    __tablename__ = 'user_note_attention'
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, nullable=False)
    # 收藏者id与user表建立多对一关系
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


# 5.帖子基本信息表
class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    create_date = db.Column(db.DateTime, nullable=False, index=True)
    note_raise = db.Column(db.Integer, nullable=True)
    down = db.Column(db.Integer, nullable=True)
    # 帖子的所有者，与users建立一对多关系
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # 与Note_content建立一对一关系
    content = db.relationship("Note_content", backref="note", uselist=False)
    # 与note_comment建立一对多关系
    comments = db.relationship("Note_comment", backref="note", lazy='dynamic')


# 6.帖子内容表
class Note_content(db.Model):
    __tablename__ = 'note_content'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(900), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    # 与Notes建立一对一关系
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), unique=True)


# 7.帖子评论表
class Note_comment(db.Model):
    __tablename__ = 'note_comment'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, index=True)
    content = db.Column(db.String(300), nullable=False)
    comment_raise = db.Column(db.Integer, nullable=True)
    down = db.Column(db.Integer, nullable=True)
    # 与notes表建立多对一关系
    note_id = db.Column(db.Integer, db.ForeignKey("notes.id"), nullable=False)
    # 与users建立多对一关系
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self):
        dict={
            "head_path":self.user.head_path,
            "name":self.user.name,
            "comment_content":self.content,
            "date":self.date,
            "raise":self.comment_raise,
            "down":self.down
        }
        return dict
