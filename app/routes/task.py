# -*- coding: utf-8 -*-
from flask import Blueprint, request, Response
from queue import Queue
from app.core.task_thread import async_task_wrapper
from app.scripts import *

task_bp = Blueprint("task", __name__)
task_logs = {}

# 命令组装
def build_system_commands(opts):
    cmds = []
    if opts.get("yum_repo"):cmds += yum_repo.get_commands()
    if opts.get("ntp"):cmds += ntp.get_commands(opts.get("ntp_server"))
    if opts.get("firewall"):cmds += firewall.get_commands()
    if opts.get("ssh_optimize"):cmds += ssh_optimize.get_commands()
    if opts.get("stop_services"):cmds += stop_services.get_commands()
    if opts.get("numa_thp"):cmds += numa_thp.get_commands()
    if opts.get("swap"):cmds += swap.get_commands()
    if opts.get("limits"):cmds += limits.get_commands()
    if opts.get("history"):cmds += history.get_commands()
    if opts.get("kernel"):cmds += kernel.get_commands()
    if opts.get("ipv6"):cmds += ipv6.get_commands()
    if opts.get("tools"):cmds += tools.get_commands(opts.get("tools_list"))
    if opts.get("container"):cmds += container.get_commands()
    return cmds

def build_env_commands(opts):
    cmds = []
    if opts.get("java"):cmds.extend(java.get_commands(opts.get("java_version")))
    if opts.get("docker"):cmds.extend(docker.get_commands())
    return cmds

@task_bp.route("/run", methods=["POST"])
def run_task():
    data = request.json
    msg_queue = Queue(maxsize=500)
    async_task_wrapper(data, msg_queue, build_system_commands, build_env_commands)
    def generate():
        while True:
            item = msg_queue.get()
            if item is None:break
            yield item + "\n"
    return Response(generate(), mimetype="application/json")

@task_bp.route("/export")
def export_log():
    txt = ""
    for k, v in task_logs.items():
        txt += f"===== 服务器：{v['host']} =====\n{v['log']}\n\n"
    return Response(txt, mimetype="text/plain", headers={"Content-Disposition": "attachment; filename=服务器初始化日志.txt"})
