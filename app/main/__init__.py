"""
主业务逻辑包
与主题相关的所有业务逻辑的处理（发表，查看，修改，删除）
"""
from flask import Blueprint

main = Blueprint("main", __name__)
from . import views