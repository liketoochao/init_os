# -*- coding: utf-8 -*-
# @Author : Admin
# @Time   : 2026
# @Desc   : Java离线安装（项目默认包 / 用户上传包）
import os
import subprocess
import shutil

def install_java(java_source_path: str = None):
    """
    Java 离线安装
    优先使用：项目自带 app/files/jdk-8u471-linux-x64.tar
    也支持传入用户上传路径：java_source_path="xxx.tar"
    安装到：/opt/jdk
    """
    # ==================== 1. 确定JDK包路径 ====================
    # 默认项目内置路径
    default_jdk = os.path.join(os.path.dirname(os.path.dirname(__file__)), "files", "jdk-8u471-linux-x64.tar")

    # 如果用户传入了路径，则使用用户上传的包
    if java_source_path and os.path.exists(java_source_path):
        jdk_file = java_source_path
        print(f"[+] 使用用户上传的JDK包: {jdk_file}")
    else:
        jdk_file = default_jdk
        print(f"[+] 使用项目默认JDK包: {jdk_file}")

    # 检查文件是否存在
    if not os.path.exists(jdk_file):
        print(f"[-] 错误：JDK文件不存在 {jdk_file}")
        return

    # ==================== 2. 复制到 /opt 目录 ====================
    target_tmp = "/opt/jdk-8u471-linux-x64.tar"
    try:
        shutil.copy(jdk_file, target_tmp)
        print(f"[+] JDK包已复制到: {target_tmp}")
    except Exception as e:
        print(f"[-] 复制JDK包失败: {e}")
        return

    install_dir = "/opt/jdk"

    # ==================== 3. 安装与配置命令 ====================
    cmds = [
        f"mkdir -p {install_dir}",
        f"tar -xvf {target_tmp} -C {install_dir} --strip-components=1",
        # 配置环境变量
        """cat >> /etc/profile <<EOF
# JAVA ENV
export JAVA_HOME=/opt/jdk
export JRE_HOME=$JAVA_HOME/jre
export CLASSPATH=.:$JAVA_HOME/lib:$JRE_HOME/lib
export PATH=$PATH:$JAVA_HOME/bin
EOF""",
        "source /etc/profile",
        "java -version"
    ]

    for cmd in cmds:
        try:
            subprocess.run(cmd, shell=True, check=False)
        except Exception as e:
            print(f"[-] 执行失败: {cmd}, 错误: {e}")

    print("[+] Java 安装完成！\n")


if __name__ == '__main__':
    install_java()
