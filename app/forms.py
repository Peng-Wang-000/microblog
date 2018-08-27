# -*-coding:utf8-*-

# API已经改变了 from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


# 登录表单
class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
