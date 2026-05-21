def get_commands(tools_list="lsof vim wget curl tar git"):
    return [
        f"dnf install -y {tools_list} -q",
    ]
