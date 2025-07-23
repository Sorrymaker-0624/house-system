import json
from flask import Blueprint, request, Response, jsonify

from models import User
from config import db

user_api = Blueprint('user_api', __name__)

@user_api.route('/register', methods=['POST'])
def register():
    # 获取用户名
    username = request.form['username']
    # 密码
    password = request.form['password']
    # 邮箱
    email = request.form['email']

    # 检查数据库当中是否存在该用户
    result = User.query.filter(User.name == username).all()

    # 如果查询出来的数据长度为0的话，则该用户名没有被注册过
    if len(result) == 0:
        user = User(name=username, password=password, email=email)
        # 将用户对象添加到数据库中
        db.session.add(user)
        db.session.commit()

        json_str = json.dumps({'valid':1, 'msg':user.name})
        # 实例化的过程需要给他传入响应的内容
        res = Response(json_str)
        res.set_cookie('name', user.name, 3600 * 2)
        return res
    else:
        return jsonify({'valid':0, 'msg': '该用户已被注册'})

# 用户登录
@user_api.route('/login',methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # 查询用户是否存在
    user = User.query.filter(User.name == username).first()
    # 如果用户存在
    if user:
        # 判断密码是否相等
        if user.password == password:
            result = {'valid':1,'msg':user.name}
            result_json = json.dumps(result)
            res = Response(result_json)
            res.set_cookie('name', user.name, 3600 * 2)
            return res
        else:
            return jsonify({'valid':0, 'msg': '密码错误'})
    else:
        return jsonify({'valid': 0, 'msg': '用户不存在'})
    
# 退出登录
@user_api.route('/logout')
def logout():
    # 先从cookie中获取用户信息
    name = request.cookies.get('name')
    if name:
        res = jsonify({'valid': 1, 'msg': '退出登录成功'}) # 使用 jsonify
        res.delete_cookie('name') # jsonify返回的也是一个Response对象，可以继续操作
        return res
    else:
        return jsonify({'valid':0, 'msg':'未登录'})