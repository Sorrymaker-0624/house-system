import json
from flask import Blueprint, request, Response, jsonify

from models import User,House
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
    
@user_api.route('/collect/<int:house_id>', methods=['POST'])
def toggle_collection(house_id):
    """
    处理收藏与取消收藏的切换逻辑。
    """
    # 1. 检查用户是否已登录（我们约定使用session）
    user_name = request.cookies.get('name')
    if not user_name:
         return jsonify({'valid': '0', 'msg': '请先登录'})
    user = User.query.filter_by(name=user_name).first()

    # （可选）检查房源是否存在，确保数据安全
    house = House.query.get(house_id)
    if not house:
        return jsonify({'valid': '0', 'msg': '操作的房源不存在'})

    # 3. 获取用户当前的收藏列表
    #    - 如果 user.collect_id 存在且不为空，则按','分割成列表
    #    - 否则，创建一个空列表
    collect_ids = user.collect_id.split(',') if user.collect_id and user.collect_id != '' else []
    
    # 4. 判断是“收藏”还是“取消收藏”
    str_house_id = str(house_id) # ID在列表中是以字符串形式存在的，需要转换

    if str_house_id in collect_ids:
        # 如果ID已存在 -> 执行【取消收藏】操作
        collect_ids.remove(str_house_id)
        action = 'removed'
        msg = '已取消收藏'
    else:
        # 如果ID不存在 -> 执行【添加收藏】操作
        collect_ids.append(str_house_id)
        action = 'added'
        msg = '收藏成功'
    
    # 5. 将更新后的列表重新拼接成字符串，并保存回数据库
    try:
        user.collect_id = ','.join(collect_ids)
        db.session.commit()
        # 6. 返回成功的响应，并告诉前端具体执行了什么操作（'action'字段）
        return jsonify({'valid': '1', 'msg': msg, 'action': action})
    except Exception as e:
        db.session.rollback() # 如果出错，回滚数据库操作
        return jsonify({'valid': '0', 'msg': f'数据库错误: {e}'})