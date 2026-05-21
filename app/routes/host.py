# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, session
import json
import os

host_bp = Blueprint("host", __name__, url_prefix="/host")

# 主机信息存储文件（存在服务器上）
HOST_FILE = "hosts.json"

# 初始化文件
if not os.path.exists(HOST_FILE):
    with open(HOST_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)


# 1. 添加主机（登录后才能用）
@host_bp.route("/add", methods=["POST"])
def add_host():
    # 验证是否登录
    if "user" not in session:
        return jsonify({"code": 403, "msg": "请先登录"}), 403

    # 获取前端传过来的主机信息
    data = request.json
    name = data.get("name")
    ip = data.get("ip")
    port = data.get("port", 22)
    username = data.get("username")
    password = data.get("password")
    remark = data.get("remark", "")

    if not all([name, ip, username, password]):
        return jsonify({"code": 400, "msg": "信息不完整"}), 400

    # 读取服务器上的主机列表
    with open(HOST_FILE, "r", encoding="utf-8") as f:
        hosts = json.load(f)

    # 新主机信息
    new_host = {
        "name": name,
        "ip": ip,
        "port": port,
        "username": username,
        "password": password,
        "remark": remark,
        "create_user": session["user"]
    }

    # 添加并保存回文件
    hosts.append(new_host)
    with open(HOST_FILE, "w", encoding="utf-8") as f:
        json.dump(hosts, f, ensure_ascii=False, indent=4)

    return jsonify({"code": 200, "msg": "主机添加成功！"})


# 2. 获取当前用户的主机列表
@host_bp.route("/list", methods=["GET"])
def host_list():
    if "user" not in session:
        return jsonify({"code": 403, "msg": "请先登录"}), 403

    with open(HOST_FILE, "r", encoding="utf-8") as f:
        hosts = json.load(f)

    # 只返回自己添加的主机
    user_hosts = [h for h in hosts if h.get("create_user") == session["user"]]
    return jsonify({"code": 200, "data": user_hosts})
