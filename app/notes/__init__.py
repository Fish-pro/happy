"""
处理发帖相关操作
"""
from flask import Blueprint

notes = Blueprint("notes", __name__)
from . import views