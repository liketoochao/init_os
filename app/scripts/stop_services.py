def get_commands():
    return [
        "systemctl disable --now postfix avahi-daemon cups 2>/dev/null",
    ]
