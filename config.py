# -*- coding: utf-8 -*-
"""全局配置文件"""
import os

# 基础配置
SECRET_KEY = "centos9-wizard-v3-2026-flask"
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# 登录账号密码（统一管理）
USERNAME = "admin"
PASSWORD = "admin"

# 路径配置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
