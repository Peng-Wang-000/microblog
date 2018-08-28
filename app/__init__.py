from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(Config)

# 数据库在应用的表现形式是一个数据库实例，数据库迁移引擎同样如此,它们将会在应用实例化之后进行实例化和注册操作。
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models