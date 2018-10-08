from datetime import datetime
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


# 为flask-Login准备用户模型
# 添加loginmanager的混入UserMixin相当于添加了必须的四个选项--完成用户认证
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # User类中创建的db.relationship为用户添加了posts属性，并为用户动态（Post）添加了author属性。 我使用author虚拟字段来调用其作者，而不必通过用户ID来处理。
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # __repr__方法用于在调试时打印用户实例
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # 加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 判断是否相等
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

# 用户发表的动态
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_id字段被初始化为user.id的外键，这意味着它引用了来自用户表的id值。本处的user是数据库表的名称，Flask-SQLAlchemy自动设置类名为小写来作为对应表的名称。
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# 用户加载函数 @login.user_loader装饰器来为用户加载功能注册函数。将获取的user加入用户会话中
# Flask-Login将字符串类型的参数id传入用户加载函数，因此使用数字ID的数据库需要如上所示地将字符串转换为整数。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
