def get_commands():
    return [
        "grubby --update-kernel=ALL --args=\"numa=off transparent_hugepage=never\"",
        "echo never > /sys/kernel/mm/transparent_hugepage/enabled",
        "echo never > /sys/kernel/mm/transparent_hugepage/defrag",
    ]
