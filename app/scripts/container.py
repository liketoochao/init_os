def get_commands():
    return [
        "modprobe overlay",
        "modprobe br_netfilter",
        "echo 'net.ipv4.ip_forward = 1' >> /etc/sysctl.conf",
        "echo 'net.bridge.bridge-nf-call-iptables = 1' >> /etc/sysctl.conf",
        "sysctl -p",
    ]
