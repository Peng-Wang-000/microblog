from app import app, db
from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    # current_user主要从用户会话中拿到当前用户
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # 从数据库查询用户
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
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    # 该函数会将用户登录状态注册为未登录，表现会is_anonymous为TRUE
    logout_user()
    return redirect(url_for('index'))


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