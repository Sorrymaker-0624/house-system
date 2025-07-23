# 配置文件

from flask_sqlalchemy import SQLAlchemy 
import os


# 创建flask_sqlalchemy的实例对象
db = SQLAlchemy()

class Config:
    # 调试模式
    DEBUG = False
    # 指定数据库的连接地址 -使用SQLite数据库
    # 获取当前文件所在目录
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "house.db")}' 
    # 关闭警告提示
    SQLALCHEMY_TRACK_MODIFICATIONS = True