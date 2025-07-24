from flask import Blueprint, render_template, redirect

from models import User ,House, Recommend
from config import db
user_page=Blueprint('user_page', __name__)

# 用户中心页面
@user_page.route('/user/<username>')
def user(username):
    user = User.query.filter(User.name == username).first()
    
    if user:
        # --- 查询收藏的房源 (这部分代码是正确的) ---
        collect_house_list = []
        if user.collect_id:
            collect_ids = user.collect_id.split(',')
            valid_ids = [int(id_str) for id_str in collect_ids if id_str]
            if valid_ids:
                collect_house_list = House.query.filter(House.id.in_(valid_ids)).all()

        seen_house_list = db.session.query(House).join(
            Recommend, House.id == Recommend.house_id
        ).filter(
            Recommend.user_id == user.id
        ).order_by(
            Recommend.score.desc()
        ).limit(10).all()

        return render_template(
            'user_page.html', 
            user=user, 
            collect_house_list=collect_house_list,
            seen_house_list=seen_house_list
        )

    else:
        return redirect('/')