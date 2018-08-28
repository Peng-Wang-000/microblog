# 基本概念

## microblog.py
    主运行程序
## config.py
    配置文件
## app.db
    数据库文件
## migrations
    数据库迁移文件夹
    
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

    
    