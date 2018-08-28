from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required  # 确保了这页只被已经登录的用户看到
def index():
    user = g.user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    # 判断用户是否登录 g.user.is_authenticated() to g.user.is_authenticated
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # 处理获取的表单内容
    if form.validate_on_submit():
        # 存储
        session['remember_me'] = form.remember_me.data
        # oid.try_login 被调用是为了触发用户使用 Flask-OpenID 认证。
        # 该函数有两个参数，用户在 web 表单提供的 openid 以及我们从 OpenID 提供商得到的数据项列表。
        # 因为我们已经在用户模型类中定义了 nickname 和 email，这也是我们将要从 OpenID 提供商索取的。
        # OpenID 认证异步发生。如果认证成功的话，Flask-OpenID 将会调用一个注册了 oid.after_login 装饰器的函数。如果失败的话，用户将会回到登陆页面。
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    # 表单渲染部分
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# 从数据库加载用户,这个函数将会被 Flask-Login 使用
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# OpenID认证成功 resp 参数传入给 after_login 函数，它包含了从 OpenID 提供商返回来的信息。
@oid.after_login
def after_login(resp):
    # 从OpenID提供商返回来的信息
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    # 判断数据库中是否有user信息
    user = User.query.filter_by(email=resp.email).first()
    # 认为是新用户
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False

    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


# 全局变量 current_user 是被 Flask-Login 设置的，因此我们只需要把它赋给 g.user ，让访问起来更方便。
@app.before_request
def before_request():
    g.user = current_user
