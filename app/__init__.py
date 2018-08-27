from flask import Flask

# 创建了flask实例对象
app = Flask(__name__)
# 加载配置文件
app.config.from_object('config')

from app import views
