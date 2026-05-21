# -*- coding: utf-8 -*-
# @Author : Admin
# @Time   : 2026
# @Desc   : Docker+Compose 国内静态源 无外网 适配CentOS9
def get_commands():
    cmds = [
        # 基础依赖
        "dnf install -y yum-utils device-mapper-persistent-data lvm2 -q",
        # 更换国内可用docker源（避开阿里云失效域名）
        "yum-config-manager --add-repo https://docker.mirrors.ustc.edu.cn/linux/centos/docker-ce.repo",
        # 安装docker
        "dnf install -y docker-ce docker-ce-cli containerd.io -q",
        # 开机自启
        "systemctl enable docker && systemctl start docker",
        # 国内镜像加速（永久可用）
        """mkdir -p /etc/docker && tee /etc/docker/daemon.json <<EOF
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com"
  ]
}
EOF""",
        "systemctl daemon-reload && systemctl restart docker",
        # 【关键】国内镜像站下载docker-compose，抛弃无法访问的github
        "curl -L https://download.fastgit.org/docker/compose/releases/download/v2.29.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose",
        "chmod +x /usr/local/bin/docker-compose",
        "ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose",
        # 补全
        "dnf install -y bash-completion -q",
        "source /usr/share/bash-completion/completions/docker",
        # 版本查看
        "docker --version",
        "docker-compose --version"
    ]
    return cmds
