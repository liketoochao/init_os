# -*- coding: utf-8 -*-
from flask import Flask
from config import SECRET_KEY


def create_app():
    app = Flask(__name__)

    # 密钥（session登录必须）
    app.secret_key = SECRET_KEY

    # 注册所有蓝图
    from app.routes.auth import auth_bp  # 登录相关
    from app.routes.task import task_bp  # 任务执行相关
    from app.routes.host import host_bp  # 主机管理（新增）

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(host_bp)

    return app
