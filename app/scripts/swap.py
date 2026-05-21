def get_commands():
    return [
        "swapoff -a",
        "sed -i '/swap/s/^/#/' /etc/fstab",
    ]
