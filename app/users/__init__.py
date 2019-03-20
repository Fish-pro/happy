"""
处理与用户相关的业务逻辑包（用户注册，用户登录，用户登出）
"""
from flask import Blueprint

users = Blueprint("users", __name__)
from . import views