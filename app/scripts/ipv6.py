def get_commands():
    return [
        "echo 'net.ipv6.conf.all.disable_ipv6 = 1' >> /etc/sysctl.conf",
        "sysctl -p",
    ]
