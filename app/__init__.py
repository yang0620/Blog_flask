# 对整个应用程序做初始化操作
# 主要工作：
# 1.创建Flask应用以及各种配置
# 2.创建数据库实例-SQLAlchemy的实例
# 3.通过蓝图(Blueprint)关联其他的业务程序

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

# 创建数据库实例
db = SQLAlchemy()


# 通过一个函数创建app
def create_app():
    app = Flask(__name__)

    # 有关app的配置
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/blog'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SECRET_KEY'] = 'xieshadouxing'

    # 使用app初始化db(数据库实例)
    db.init_app(app)

    # 使用蓝图(Blueprint)关联程序
    # 关联main
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    # 关联users
    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    return app
