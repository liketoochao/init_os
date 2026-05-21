# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, redirect, session
from config import USERNAME, PASSWORD

auth_bp = Blueprint("auth", __name__)

# 登录拦截器
def login_required(f):
    def w(*args, **kwargs):
        if not session.get("login"):
            return redirect("/login")
        return f(*args, **kwargs)
    w.__name__ = f.__name__
    return w

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["login"] = True
            return redirect("/")
        return "<h3>账号密码错误</h3>"
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@auth_bp.route("/")
@login_required
def index():
    return render_template("index.html")
