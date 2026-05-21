def get_commands(ntp_server="ntp.aliyun.com"):
    return [
        "dnf install -y chrony -q",
        f"sed -i 's/^pool .*/pool {ntp_server} iburst/' /etc/chrony.conf",
        "systemctl restart chronyd",
        "systemctl enable chronyd -q",
        "timedatectl set-timezone Asia/Shanghai",
    ]
