import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
# 创建了flask实例对象
app = Flask(__name__)
# 加载配置文件
app.config.from_object('config')
db = SQLAlchemy(app)

# 使用登录管理器
lm = LoginManager()
lm.init_app(app)
# Flask-Login 需要知道哪个视图允许用户登录
lm.login_view = 'login'

# Flask-OpenID 扩展需要一个存储文件的临时文件夹的路径
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models
