from flask import Blueprint, request, jsonify
from models import User, House, db

# 1. 为收藏功能创建一个全新的蓝图(Blueprint)
collection_api = Blueprint('collection_api', __name__)



@collection_api.route('/collect/<int:house_id>', methods=['POST'])
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

    #  获取用户当前的收藏列表

    collect_ids = user.collect_id.split(',') if user.collect_id and user.collect_id != '' else []
    
    #  判断是“收藏”还是“取消收藏”
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
    
    #  将更新后的列表重新拼接成字符串，并保存回数据库
    try:
        user.collect_id = ','.join(collect_ids)
        db.session.commit()
        #  返回成功的响应，并告诉前端具体执行了什么操作（'action'字段）
        return jsonify({'valid': '1', 'msg': msg, 'action': action})
    except Exception as e:
        db.session.rollback() # 如果出错，回滚数据库操作
        return jsonify({'valid': '0', 'msg': f'数据库错误: {e}'})