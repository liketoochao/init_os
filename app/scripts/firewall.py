def get_commands():
    return [
        "systemctl stop firewalld",
        "systemctl disable firewalld -q",
        "sed -i 's/^SELINUX=.*/SELINUX=disabled/' /etc/selinux/config",
        "setenforce 0 2>/dev/null",
    ]
