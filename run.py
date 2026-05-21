# -*- coding: utf-8 -*-
"""项目启动入口，简洁干净"""
from app import create_app
from config import HOST, PORT, DEBUG

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
