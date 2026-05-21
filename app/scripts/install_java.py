# -*- coding: utf-8 -*-
# @Author : Admin
# @Time   : 2026
# @Desc   : Java环境安装 + 环境变量配置

def get_commands(version: str = "java-1.8.0-openjdk-devel"):
    cmds = [
        f"dnf install -y {version} -q",
        "mkdir -p /usr/local/java",
        """cat >> /etc/profile <<EOF
# JAVA ENV
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin
EOF""",
        "source /etc/profile",
        "java -version"
    ]
    return cmds
