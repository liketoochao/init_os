# -*- coding: utf-8 -*-
from flask import Flask
from config import SECRET_KEY
from app.routes.auth import auth_bp
from app.routes.task import task_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    # 注册蓝图（路由拆分）
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
