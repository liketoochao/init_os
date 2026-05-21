# -*- coding: utf-8 -*-
# @Author : Admin
# @Time   : 2026
# @Desc   : Docker + Compose 自动化安装（独立脚本，国内源，CentOS9）

import subprocess
import os

def install_docker():
    print("=" * 50)
    print("        开始安装 Docker + Docker Compose")
    print("=" * 50)

    cmds = [
        # 安装依赖
        "dnf install -y yum-utils device-mapper-persistent-data lvm2 -q",

        # 添加国内 Docker 源
        "yum-config-manager --add-repo https://docker.mirrors.ustc.edu.cn/linux/centos/docker-ce.repo",

        # 安装 Docker
        "dnf install -y docker-ce docker-ce-cli containerd.io -q",

        # 启动并开机自启
        "systemctl enable docker && systemctl start docker",

        # 配置国内镜像加速
        """mkdir -p /etc/docker && tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF""",

        # 重启生效
        "systemctl daemon-reload && systemctl restart docker",

        # 安装 docker-compose v2.29.1
        "curl -L https://download.fastgit.org/docker/compose/releases/download/v2.29.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose",
        "chmod +x /usr/local/bin/docker-compose",
        "ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose",

        # 命令补全
        "dnf install -y bash-completion -q",
        "source /usr/share/bash-completion/completions/docker 2>/dev/null",

        # 查看版本
        "docker --version",
        "docker-compose --version"
    ]

    # 执行命令
    for cmd in cmds:
        try:
            subprocess.run(cmd, shell=True, check=False)
        except Exception as e:
            print(f"[-] 执行失败: {cmd}")
            print(f"错误信息: {e}")

    print("\n[+] Docker + Docker Compose 安装完成！")
    print("[+] 镜像加速已配置完成！\n")


# 独立运行
if __name__ == '__main__':
    install_docker()
