# CentOS 初始化脚本包
# 所有功能已合并到 os_initializer.py 的 InitOS 类中

from .os_initializer import InitOS

# 安装类脚本独立导出
from .install_docker import install_docker
from .install_java import install_java
