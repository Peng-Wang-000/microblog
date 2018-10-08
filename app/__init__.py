from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
# 通知Flask读取配置文件内容
app.config.from_object(Config)

# 数据库和迁移引擎 将会在应用实例化之后进行实例化和注册操作。
# db对象来表示数据库
db = SQLAlchemy(app)
# 数据库迁移引擎
migrate = Migrate(app, db)

# 登录管理器
login_manager = LoginManager(app)
# 指定登录认证视图,等价于url_for('login')
login_manager.login_view = 'login'


# 将组件注入到程序中,解决循环应用的问题
from app import routes, models, errors
