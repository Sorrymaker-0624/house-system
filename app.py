# 项目入口文件
from flask import Flask, render_template

from api.user import user_api
from config import Config, db

# 首页
from page.index import index_page
# 搜索页
from page.query import query_page 
# 列表页
from page.list import list_page
# 详情页
from page.detail import detail_page
# 详情页API
from api.detail import detail_api
# 用户中心页面
from page.user import user_page
# 浏览记录
from api.history_api import history_api 
# 收藏
from api.collection_api import collection_api
# 编辑
from api.userinfo import userinfo_api
app =Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 测试代码
# @app.route('/')
# def hello():
#     first_house = House.query.first()
#     print(first_house)

#     return render_template('index.html')

# 注册首页
app.register_blueprint(index_page, url_prefix='/')
# 注册搜索页
app.register_blueprint(query_page, url_prefix='/')
# 注册列表页
app.register_blueprint(list_page, url_prefix='/')
# 注册详情页
app.register_blueprint(detail_page, url_prefix='/')
# 注册用户中心页面
app.register_blueprint(user_page, url_prefix='/')
# 注册详情页API
app.register_blueprint(detail_api, url_prefix='/get/')
# 注册用户登录与注册接口
app.register_blueprint(user_api, url_prefix='/')
# 浏览记录接口
app.register_blueprint(history_api, url_prefix='/')
# 收藏接口
app.register_blueprint(collection_api, url_prefix='/')
# 编辑接口
app.register_blueprint(userinfo_api,url_prefix='/modify/userinfo')
if __name__ == '__main__':
    app.run(debug=True)