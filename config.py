import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 使用类来存储配置变量
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Flask-SQLAlchemy插件(ORM框架)从SQLALCHEMY_DATABASE_URI配置变量中获取应用的数据库的位置。
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS配置项用于设置数据发生变更之后是否发送信号给应用，我不需要这项功能，因此将其设置为False。
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 邮件服务
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # 启用加密连接的布尔标记
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS配置变量是将收到错误报告的电子邮件地址列表，所以你自己的电子邮件地址应该在该列表中。
    ADMINS = ['1455044898@qq.com']
