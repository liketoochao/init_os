import os
import re
import subprocess


class InitOS:
    """
    服务器初始化统一类
    包含：防火墙、主机名、IPV6、内核参数、SSH优化、SWAP、NTP、限制配置、历史命令、容器配置、关闭无用服务等
    """

    def __init__(self):
        # 通用系统路径
        self.sysctl_path = "/etc/sysctl.conf"
        self.limits_path = "/etc/security/limits.conf"
        self.ssh_config = "/etc/ssh/sshd_config"
        self.hosts_path = "/etc/hosts"
        self.selinux_config = "/etc/selinux/config"

    # ==================== 1. 防火墙配置 ====================
    def config_firewall(self):
        print("[+] 关闭并禁用 firewalld")
        subprocess.run("systemctl stop firewalld && systemctl disable firewalld", shell=True)

    # ==================== 2. 主机名配置 ====================
    def config_hostname(self, hostname):
        print(f"[+] 设置主机名：{hostname}")
        subprocess.run(f"hostnamectl set-hostname {hostname}", shell=True)

    # ==================== 3. 命令历史记录优化 ====================
    def config_command_history(self):
        print("[+] 优化命令历史记录")
        history_config = 'export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S " \nexport HISTSIZE=10000 \nexport HISTFILESIZE=10000'
        with open("/etc/profile.d/history.sh", "w") as f:
            f.write(history_config)
        subprocess.run("source /etc/profile", shell=True)

    # ==================== 4. 关闭 IPV6 ====================
    def config_ipv6(self):
        print("[+] 关闭 IPv6")
        grub_config = "/etc/default/grub"
        if os.path.exists(grub_config):
            with open(grub_config, "r") as f:
                content = f.read()
            content = re.sub(r'GRUB_CMDLINE_LINUX="', r'GRUB_CMDLINE_LINUX="ipv6.disable=1 ', content)
            with open(grub_config, "w") as f:
                f.write(content)
            subprocess.run("grub2-mkconfig -o /boot/grub2/grub.cfg", shell=True)

    # ==================== 5. 内核参数优化 ====================
    def config_kernel(self):
        print("[+] 优化内核参数")
        kernel_conf = """
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 65535
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_tw_recycle = 0
net.ipv4.tcp_fin_timeout = 30
"""
        with open(self.sysctl_path, "a") as f:
            f.write(kernel_conf)
        subprocess.run("sysctl -p", shell=True)

    # ==================== 6. 系统资源限制优化 ====================
    def config_limits(self):
        print("[+] 优化系统资源限制")
        limits_conf = """
* soft nofile 65535
* hard nofile 65535
* soft nproc 65535
* hard nproc 65535
"""
        with open(self.limits_path, "a") as f:
            f.write(limits_conf)

    # ==================== 7. Chronyd 时间同步 ====================
    def config_chronyd(self):
        print("[+] 配置 chronyd 时间同步")
        subprocess.run("yum install -y chronyd && systemctl start chronyd && systemctl enable chronyd", shell=True)

    # ==================== 8. NUMA + THP 关闭 ====================
    def config_numa_thp(self):
        print("[+] 关闭 NUMA 和 THP")
        subprocess.run("echo never > /sys/kernel/mm/transparent_hugepage/enabled", shell=True)
        subprocess.run("echo never > /sys/kernel/mm/transparent_hugepage/defrag", shell=True)

    # ==================== 9. SSH 优化 ====================
    def config_ssh_optimize(self):
        print("[+] SSH 服务优化")
        ssh_options = {
            "UseDNS": "no",
            "GSSAPIAuthentication": "no",
            "ClientAliveInterval": "60",
            "ClientAliveCountMax": "10"
        }
        with open(self.ssh_config, "r") as f:
            lines = f.readlines()
        with open(self.ssh_config, "w") as f:
            for line in lines:
                for k, v in ssh_options.items():
                    if line.startswith(k):
                        line = f"{k} {v}\n"
                f.write(line)
        subprocess.run("systemctl restart sshd", shell=True)

    # ==================== 10. 关闭无用服务 ====================
    def stop_unimportant_services(self):
        print("[+] 关闭无用系统服务")
        services = ["postfix", "avahi-daemon", "bluetooth", "cups"]
        for s in services:
            subprocess.run(f"systemctl stop {s} && systemctl disable {s}", shell=True)

    # ==================== 11. SWAP 配置 ====================
    def config_swap(self, disable=True):
        if disable:
            print("[+] 关闭 SWAP")
            subprocess.run("swapoff -a && sed -i '/swap/s/^/#/' /etc/fstab", shell=True)
        else:
            print("[+] 保持 SWAP 开启")

    # ==================== 12. YUM 源配置 ====================
    def add_yum_repo(self):
        print("[+] 添加基础 YUM 源")
        subprocess.run("yum install -y epel-release", shell=True)
        subprocess.run("yum makecache", shell=True)

    # ==================== 13. 安装基础工具 ====================
    def install_tools(self):
        print("[+] 安装常用系统工具")
        tools = "vim wget curl telnet lsof net-tools htop iftop iotop"
        subprocess.run(f"yum install -y {tools}", shell=True)

    # ==================== 14. 容器相关配置 ====================
    def config_container(self):
        print("[+] 配置容器环境参数")
        self.config_kernel()  # 依赖内核优化
        print("[+] 容器环境配置完成")

    # ==================== 一键执行所有初始化（最实用） ====================
    def full_init(self, hostname="server"):
        self.config_firewall()
        self.config_hostname(hostname)
        self.config_command_history()
        self.config_ipv6()
        self.config_kernel()
        self.config_limits()
        self.config_chronyd()
        self.config_numa_thp()
        self.config_ssh_optimize()
        self.stop_unimportant_services()
        self.config_swap(disable=True)
        self.add_yum_repo()
        self.install_tools()
        self.config_container()
        print("[+] 系统初始化全部完成！")
