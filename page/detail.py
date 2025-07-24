from flask import Blueprint, render_template ,request

from models import House,User,Recommend
from config import db
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
    
    if user_name:
        user = User.query.filter_by(name=user_name).first()
        if user and user.collect_id:
            collect_ids = user.collect_id.split(',')
            if str(hid) in collect_ids:
                is_collected = True
    
   
    if user_name: # 同样，只有在用户登录时才记录
        # a. 查找是否已有这条用户对这个房源的浏览记录
        record = Recommend.query.filter_by(user_id=user.id, house_id=hid).first()
        
        if record:
            # b. 如果记录已存在，说明是重复访问，将分数(score)+1
            record.score += 1
        else:
            # c. 如果记录不存在，就创建一条新记录
            record = Recommend(
                user_id=user.id,
                house_id=hid,
                title=house.title,
                address=house.address,
                block=house.block,
                score=1 # 首次访问，分数为1
            )
        # d. 将修改或新增的记录提交到数据库
        db.session.add(record)
        db.session.commit()
    # 最后，把 is_collected 这个状态变量传递给前端模板
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