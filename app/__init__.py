from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 创建了flask实例对象
app = Flask(__name__)
# 加载配置文件
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
