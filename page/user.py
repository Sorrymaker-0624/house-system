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

        # ================================================================
        # ▼▼▼▼▼▼▼▼▼▼ 【关键修改】更新查询浏览记录的逻辑 ▼▼▼▼▼▼▼▼▼▼
        # ================================================================
        
        # 使用JOIN查询，将Recommend表和House表连接起来
        # 这样可以直接获取到完整的House对象，并且还能按浏览次数(score)排序
        seen_house_list = db.session.query(House).join(
            Recommend, House.id == Recommend.house_id
        ).filter(
            Recommend.user_id == user.id
        ).order_by(
            Recommend.score.desc()
        ).limit(10).all()

        # =======================================================
        # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
        # =======================================================
        
        # --- 将所有查询到的数据传递给模板 ---
        return render_template(
            'user_page.html', 
            user=user, 
            collect_house_list=collect_house_list,
            seen_house_list=seen_house_list # 现在这里面是完整的House对象了
        )

    else:
        return redirect('/')