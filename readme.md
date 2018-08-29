# 基本概念

## 主运行程序
   microblog.py
## 配置文件
   config.py
## 数据库文件
   app.db
## 数据库迁移文件夹
    migrations
    
## app
    static:静态文件
    templates:模板文件
    __init__.py：初始化文件
    forms.py:表单对象，用于页面展示
    models.py:模型对象与数据库进行ORM的对象
    routes.py:前端页面路由

# 数据持久化
## 数据库
SQLite：Python自带的数据库
## ORM
- 安装 :(venv) $ pip install flask-sqlalchemy
Flask-SQLAlchemy，这个插件为流行的SQLAlchemy包做了一层封装以便在Flask中调用更方便，类似SQLAlchemy这样的包叫做Object Relational Mapper，简称ORM。 
ORM允许应用程序使用高级实体（如类，对象和方法）而不是表和SQL来管理数据库。 ORM的工作就是将高级操作转换成数据库命令。

## 数据库迁移
- 安装:(venv) $ pip install flask-migrate
Flask-Migrate。 这个插件是Alembic的一个Flask封装，是SQLAlchemy的一个数据库迁移框架。 
使用数据库迁移增加了启动数据库时候的一些工作，但这对将来的数据库结构稳健变更来说，是一个很小的代价。

## 数据库迁移操作
- 创建数据库迁移存储库  (venv) $ flask db init
- 数据库迁移 (venv) $ flask db migrate -m "users table"
- 更改应用到数据库 (venv) $ flask db upgrade
    
# 用户账户操作
## flask插件
- WerkZeug :完成密码哈希以及url解析
- Flask-Login:该插件管理用户登录状态，以便用户可以登录到应用，然后用户在导航到该应用的其他页面时，应用会“记得”该用户已经登录。
它还提供了“记住我”的功能，允许用户在关闭浏览器窗口后再次访问应用时保持登录状态。
## 用户登入
- 为flask-login准备用户模型：采用混入的方式来将flask-login与用户模型联系起来，仅仅只需要用户模型继承其提供的
UserMixin即可，继承该类的模型会自动拥有四项属性。官方文档：https://flask-login.readthedocs.io/en/latest/
- 用户加载函数：首先需要理解的是flask为每个用户都准备存储空间，我们将其称之为用户回话，flask-login插件就是利用了该存储空间来存储用户信息（id）
每当跳转到新的页面的过程中，Flask-Login将从会话中检索用户的ID，然后将该用户实例加载到内存中。为了得到指定的用户信息，需要提供一个函数来获取用户信息。
Flask-Login插件期望应用配置一个用户加载函数，可以调用该函数来加载给定ID的用户。该函数使用@login_manager.user_loader
装饰器来指定加载用户的函数。
- 用户登入：使用login_user(user,remember)，该函数会将用户登录状态注册为已登录，这意味着用户导航到任何未来的页面时，应用通过 用户加载函数 将用户实例赋值给current_user变量。
- current_user:变量来自Flask-Login，可以在处理过程中的任何时候调用以获取用户对象。 这个变量的值可以是数据库中的一个用户对象（Flask-Login通过我上面提供的用户加载函数回调读取），或者如果用户还没有登录，则是一个特殊的匿名用户对象。
- @login_required:装饰器来拒绝匿名用户的访问以保护某个视图函数
## 用户登出
- 通过Flask-Login的logout_user()函数来实现
## 用户注册
- routes：register()
- web表单：RegistrationForm
- web模板：register.html