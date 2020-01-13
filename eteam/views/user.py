from flask import Blueprint, request, jsonify
from ..wx import getuserinfo
from eteam import db
from ..models import User

user_mod=Blueprint('user', __name__)



@user_mod.route('/getopenid', methods=["POST"])
def getopenid():
    code = request.form['code']
    try:#不会改变变量作用域
        info = getuserinfo(code)
    except:
        return jsonify(success=0, msg="openid获取失败，原因：code换取openid失败")

    success=1
    openid = info['openid']
    msg= '用户已登陆'
    # TODO 这里注释过，注册和登陆的区别

    try:
        registered=find_user(openid)
        if not registered:
            db.session.add(User(openid=openid))
            db.session.commit()
            msg= '新用户注册成功'
            return jsonify(success=success,msg=msg,openid=openid)
        else:
            msg='用户已注册，用户已登陆'
            return jsonify(success=success,msg=msg,openid=openid)
    except: 
        return jsonify(success=0, msg="openid获取失败，原因：数据库操作失败")



def find_user(openid):
    me= User.query.filter_by(openid=openid).first()
    log = open('log', 'a+')

    if(me):
        log.write('Found User'+str(me))
        # me.record_last_login()
    else:
        log.write("not find thie user"+'now me='+str(me))

    log.close()
    return me
