from flask import Blueprint, render_template ,request

from models import House,User

detail_page = Blueprint('detail_page', __name__)

@detail_page.route('/house/<int:hid>')
def detail(hid):
    # 从数据库中查找房源ID为hid的房源对象
    house = House.query.get(hid)
    # 获取房源对象的配置设施信息
    facilities_str = house.facilities
    # 将配表设施以-作为分割保存在列表facilities_list中
    facilities_list = facilities_str.split('-')

    # 定义一个用来存放推荐房源的列表变量
    recommend_li = []
    recommend_data = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).all()

    if len(recommend_data) > 6:
        recommend_li = recommend_data[:6]
    else:
        recommend_li = recommend_data
    is_collected = False    
    user_name = request.cookies.get('name') # b. 获取当前登录的用户名
    
    if user_name: # c. 如果用户已登录
        user = User.query.filter_by(name=user_name).first()
        if user and user.collect_id:
            collect_ids = user.collect_id.split(',')
            # d. 检查当前房源ID是否在用户的收藏列表里
            if str(hid) in collect_ids:
                is_collected = True # e. 如果在，就将状态设置为“已收藏”
    #
    # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
    # ================================================================

    # f. 最后，把 is_collected 这个状态变量传递给前端模板
    return render_template('detail_page.html', 
                           house=house, 
                           facilities=facilities_list, 
                           recommend_li=recommend_li,
                           is_collected=is_collected)
# 处理交通有无的情况
def deal_none(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word
    

detail_page.add_app_template_filter(deal_none, 'dealNone')