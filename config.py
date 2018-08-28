import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Flask-SQLAlchemy插件(ORM框架)从SQLALCHEMY_DATABASE_URI配置变量中获取应用的数据库的位置。
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS配置项用于设置数据发生变更之后是否发送信号给应用，我不需要这项功能，因此将其设置为False。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
