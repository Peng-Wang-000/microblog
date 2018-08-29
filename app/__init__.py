from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)

# 数据库和迁移引擎 将会在应用实例化之后进行实例化和注册操作。
# db对象来表示数据库
db = SQLAlchemy(app)
# 数据库迁移引擎
migrate = Migrate(app, db)


from app import routes, models