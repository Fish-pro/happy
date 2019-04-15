
"""
app包包含所有的程序处理相关文件（静态文件，模板文件，实体类，以及各个业务包处理）
__innt__.py:
    1.构建Flask程序实例以及配置
    2.构建SQLAchemy数据库实例
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 声明SQLAlchemy的实例
db = SQLAlchemy()


def create_app():
    # 创建flask程序实例
    app = Flask(__name__)
    # 指定各种配置
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = "suibianxie"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://York:123456@localhost:3306/blog"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 关联db和app
    db.init_app(app)
    # 连接main蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 连接users蓝图
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)
    #连接notes
    from .notes import notes as notes_blueprint
    app.register_blueprint(notes_blueprint)

    return app