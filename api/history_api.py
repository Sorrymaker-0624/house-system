from flask import Blueprint, request, jsonify
from models import User, Recommend # Recommend模型是浏览记录
from config import db

# 1. 创建一个新的蓝图(Blueprint)，专门用于处理历史记录相关的API
history_api = Blueprint('history_api', __name__)


# 2. 将“清空浏览记录”的API函数从 user_api.py 移动到这里
@history_api.route('/del_record', methods=['POST'])
def del_record():
    user_name = request.form.get('user_name')

    if request.cookies.get('name') != user_name:
        return jsonify({'valid': '0', 'msg': '无权限操作'})

    user = User.query.filter_by(name=user_name).first()
    if not user:
        return jsonify({'valid': '0', 'msg': '用户不存在'})

    try:
        Recommend.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        return jsonify({'valid': '1', 'msg': '浏览记录已清空'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'valid': '0', 'msg': f'数据库操作失败: {e}'})

# 如果未来还有“删除单条浏览记录”等功能，也可以继续添加到这个文件里