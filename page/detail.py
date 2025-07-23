from flask import Blueprint, render_template

from models import House

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

    return render_template('detail_page.html', house=house, facilities=facilities_list, recommend_li=recommend_li)

# 处理交通有无的情况
def deal_none(word):
    if len(word) == 0 or word is None:
        return '暂无信息'
    else:
        return word
    

detail_page.add_app_template_filter(deal_none, 'dealNone')