from app import app, db
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


# 请求预处理
@app.before_request
def before_request():
    if current_user.is_authenticated:
        # 在引用current_user时，Flask-Login将调用用户加载函数，该函数将运行一个数据库查询并将目标用户添加到数据库会话中。
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# 首页
@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Wang Peng'} 可以通过current_user来获取
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='HOME', posts=posts)


# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    # current_user变量来自Flask-Login，可以在处理过程中的任何时候调用以获取用户对象。
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    # form.validate_on_submit()就会获取到所有的数据，运行字段各自的验证器，全部通过之后就会返回True，这表示数据有效。
    if form.validate_on_submit():
        # 从数据库查询用户，filter_by()的结果是一个只包含具有匹配用户名的对象的查询结果集。
        user = User.query.filter_by(username=form.username.data).first()
        # 判断用户是否存在
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password ')
            return redirect(url_for('login'))
        # 该函数会将用户登录状态注册为已登录，这意味着用户导航到任何未来的页面时，应用都会将用户实例赋值给current_user变量。
        login_user(user, remember=form.remember_me.data)
        # 获取查询字符串中next参数，该参数是由flask-Login的@login_required装饰器自动封装便于登录后的重定向操作（保存需要访问的url）
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # Flask提供了一个名为url_for()的函数，它使用URL到视图函数的内部映射关系来生成URL。
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


# 退出
@app.route('/logout')
def logout():
    # 该函数会将用户登录状态注册为未登录，表现会is_anonymous为TRUE
    logout_user()
    return redirect(url_for('index'))


# 注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# 用户详情
@app.route('/user/<username>')
@login_required
def user(username):
    # 当查不到用户是返回404
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    return render_template('user.html', user=user, posts=posts)


# 用户信息编辑
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)
