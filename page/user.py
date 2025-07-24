from flask import Blueprint, render_template, redirect

from models import User ,House, Recommend

user_page=Blueprint('user_page', __name__)

# 用户中心页面
@user_page.route('/user/<username>')
def user(username):
    # --- 查询用户 (这部分是您已有的，无需改动) ---
    user = User.query.filter(User.name == username).first()

    # 如果用户存在
    if user:
        # --- 【从这里开始是我们要添加的查询逻辑】 ---

        # a. 查询用户收藏的房源列表
        collect_house_list = [] # 首先创建一个空列表，作为默认值
        if user.collect_id: # 检查用户的收藏字段 (collect_id) 是否有内容
            # 将收藏ID的字符串按逗号分割成一个ID列表
            collect_ids = user.collect_id.split(',')
            # 过滤掉可能的空字符串ID，并转换为整数
            valid_ids = [int(id_str) for id_str in collect_ids if id_str]
            if valid_ids:
                # 根据ID列表，一次性从House表查询出所有对应的房源对象
                collect_house_list = House.query.filter(House.id.in_(valid_ids)).all()

        # b. 查询用户的浏览记录列表 (因为您的HTML中也需要这个)
        seen_house_list = Recommend.query.filter(Recommend.user_id == user.id).order_by(Recommend.score.desc()).limit(10).all()
        
        # --- 【查询逻辑结束】 ---


        # c. 【重要】在渲染页面时，把新查出来的两个列表也一并传递给前端
        return render_template(
            'user_page.html', 
            user=user, 
            collect_house_list=collect_house_list,  # <-- 将收藏列表传过去
            seen_house_list=seen_house_list         # <-- 将浏览记录列表传过去
        )

    else:
        # 不存在则跳转回首页
        return redirect('/')