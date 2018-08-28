from app import db


# 使用了Flask-Login
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # 一般而言，这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证。
    @property
    def is_authenticated(self):
        return True

    # is_active 方法应该返回 True，除非是用户是无效的，比如因为他们的账号是被禁止。
    @property
    def is_active(self):
        return True

    # s_anonymous 方法应该返回 True，如果是匿名的用户不允许登录系统。
    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        # try:
        #     return unicode(self.id)
        # except NameError:
        return str(self.id)

    # 打印这个类对象
    def __repr__(self):
        return '<User %r>' % self.nickname


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % self.body
