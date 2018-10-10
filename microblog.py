import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from app import app, db
from app.models import User, Post
import os

# app.run(debug=True, port=9999)
app.run(port=9999)

# 通过电子邮件发送错误 添加邮件服务实例
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        # 创建了一个SMTPHandler实例
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Microblog Failure',
            credentials=auth,
            secure=secure)
        # 设置它的级别，以便它只报告错误及更严重级别的信息，而不是警告，常规信息或调试消息，最后将它附加到Flask的app.logger对象中。
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

# 记录日志到文件中
if not app.debug:

    # 日志文件的存储路径位于顶级目录下，相对路径为logs / microblog.log，如果其不存在，则会创建它。
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # 本处日志文件的大小限制为10KB，并只保留最后的十个日志文件作为备份。
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
