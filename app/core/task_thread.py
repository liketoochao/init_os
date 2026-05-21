# -*- coding: utf-8 -*-
import asyncio
import asyncssh
import json
from datetime import datetime
from threading import Thread

def append_log(msg):
    return f"[{datetime.now().strftime('%m-%d %H:%M:%S')}] {msg}"

async def run_single(host, port, user, pwd, sys_cmds, env_cmds, hostname_suffix, msg_queue):
    try:
        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log("🔌 正在连接服务器...")},ensure_ascii=False))
        conn_opt = {
            "host": host, "port": port, "username": user,
            "known_hosts": None, "timeout": 10, "password": pwd
        }
        conn = await asyncssh.connect(**conn_opt)
        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log("✅ 连接成功")},ensure_ascii=False))

        real_hostname = f"node_{hostname_suffix}"
        await conn.run(f"hostnamectl set-hostname {real_hostname}", check=False)
        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"✅ 主机名设置：{real_hostname}")},ensure_ascii=False))

        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log("===== 【第一步】系统初始化 =====")},ensure_ascii=False))
        for idx, cmd in enumerate(sys_cmds):
            msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"({idx+1}/{len(sys_cmds)}) {cmd[:55]}")},ensure_ascii=False))
            res = await conn.run(cmd, check=False, timeout=60)
            if res.stdout:
                msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"OUT: {res.stdout.strip()[:80]}")},ensure_ascii=False))
            if res.stderr:
                msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"ERR: {res.stderr.strip()[:80]}")},ensure_ascii=False))

        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log("===== 【第二步】运行环境部署 =====")},ensure_ascii=False))
        for idx, cmd in enumerate(env_cmds):
            msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"({idx+1}/{len(env_cmds)}) {cmd[:55]}")},ensure_ascii=False))
            res = await conn.run(cmd, check=False, timeout=60)
            if res.stdout:
                msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"OUT: {res.stdout.strip()[:80]}")},ensure_ascii=False))
            if res.stderr:
                msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"ERR: {res.stderr.strip()[:80]}")},ensure_ascii=False))

        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log("🎉 当前服务器全部配置完成！")},ensure_ascii=False))
        msg_queue.put(json.dumps({"type":"result", "host":host},ensure_ascii=False))
        conn.close()
    except Exception as e:
        msg_queue.put(json.dumps({"type":"log", "host":host, "data":append_log(f"❌ 异常：{str(e)}")},ensure_ascii=False))
        msg_queue.put(json.dumps({"type":"result", "host":host},ensure_ascii=False))

def async_task_wrapper(data, msg_queue, build_sys, build_env):
    def thread_func():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        host_list = data["hosts"]
        suffix_base = data["host_suffix"]
        tasks = []
        for idx, host in enumerate(host_list):
            hostname_suffix = f"{suffix_base}{idx+1:02d}"
            sys_cmd = build_sys(data)
            env_cmd = build_env(data)
            tasks.append(run_single(host,data["port"],data["username"],data["password"],sys_cmd,env_cmd,hostname_suffix,msg_queue))
        loop.run_until_complete(asyncio.gather(*tasks))
        msg_queue.put(None)
    Thread(target=thread_func).start()
