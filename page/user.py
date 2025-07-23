from flask import Blueprint, render_template, redirect

from models import User

user_page=Blueprint('user_page', __name__)

# 用户中心页面
@user_page.route('/user/<username>')
def user(username):
    # 查询用户
    user = User.query.filter(User.name == username).first()
    # 如果用户存在
    if user:
        # 渲染页面
        return render_template('user_page.html', user=user)
    else:
        # 不存在则跳转回首页
        return redirect('/')