def get_commands():
    return [
        """cat >> /etc/profile <<EOF
export HISTTIMEFORMAT="%Y-%m-%d %H:%M:%S `whoami` "
EOF""",
        "source /etc/profile",
    ]
