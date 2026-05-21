def get_commands(hostname="node"):
    return [
        f"hostnamectl set-hostname {hostname}",
    ]
