from flask import Blueprint, request, jsonify, make_response
from models import db, User

userinfo_api = Blueprint('userinfo_api', __name__)

# 修改昵称
@userinfo_api.route('/name', methods=['POST'])
def modify_name():
    new_name = request.form.get('name')
    y_name = request.form.get('y_name')
    if not new_name or not y_name:
        return jsonify({'ok': '0', 'msg': '参数缺失'})
    user = User.query.filter_by(name=y_name).first()
    if not user:
        return jsonify({'ok': '0', 'msg': '用户不存在'})
    if User.query.filter_by(name=new_name).first():
        return jsonify({'ok': '0', 'msg': '昵称已被占用'})
    if new_name == user.password:
        return jsonify({'ok': '0', 'msg': '新用户名不能和密码相同'})
    user.name = new_name
    try:
        db.session.commit()
        resp = make_response(jsonify({'ok': '1', 'msg': '修改成功'}))
        resp.set_cookie('name', new_name)
        return resp
    except Exception:
        db.session.rollback()
        return jsonify({'ok': '0', 'msg': '数据库错误'})

# 修改住址
@userinfo_api.route('/addr', methods=['POST'])
def modify_addr():
    new_addr = request.form.get('addr')
    y_name = request.form.get('y_name')
    if not new_addr or not y_name:
        return jsonify({'ok': '0', 'msg': '参数缺失'})
    user = User.query.filter_by(name=y_name).first()
    if not user:
        return jsonify({'ok': '0', 'msg': '用户不存在'})
    user.addr = new_addr
    try:
        db.session.commit()
        return jsonify({'ok': '1', 'msg': '修改成功'})
    except Exception:
        db.session.rollback()
        return jsonify({'ok': '0', 'msg': '数据库错误'})

# 修改密码
@userinfo_api.route('/pd', methods=['POST'])
def modify_password():
    new_pd = request.form.get('pd')
    y_name = request.form.get('y_name')
    if not (new_pd and 6 <= len(new_pd) <= 15):
        return jsonify({'ok': '0', 'msg': '密码长度必须为6-15位'})
    if not new_pd or not y_name:
        return jsonify({'ok': '0', 'msg': '参数缺失'})
    user = User.query.filter_by(name=y_name).first()
    if not user:
        return jsonify({'ok': '0', 'msg': '用户不存在'})
    if new_pd == user.name:
        return jsonify({'ok': '0', 'msg': '新密码不能和用户名相同'})
    user.password = new_pd
    try:
        db.session.commit()
        return jsonify({'ok': '1', 'msg': '修改成功'})
    except Exception:
        db.session.rollback()
        return jsonify({'ok': '0', 'msg': '数据库错误'})

# 修改邮箱
@userinfo_api.route('/email', methods=['POST'])
def modify_email():
    new_email = request.form.get('email')
    y_name = request.form.get('y_name')
    if not new_email or not y_name:
        return jsonify({'ok': '0', 'msg': '参数缺失'})
    user = User.query.filter_by(name=y_name).first()
    if not user:
        return jsonify({'ok': '0', 'msg': '用户不存在'})
    user.email = new_email
    try:
        db.session.commit()
        return jsonify({'ok': '1', 'msg': '修改成功'})
    except Exception:
        db.session.rollback()
        return jsonify({'ok': '0', 'msg': '数据库错误'})
