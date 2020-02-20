from flask import Blueprint, request, jsonify
from eteam import db, photos
from ..models import Team, TeamImage
from ..settings import UPLOADED_PHOTO_DEST
from .user import find_user
import random, string, json, os

team_mod = Blueprint("team", __name__)


@team_mod.route('/create_team', methods=['POST'])
def create_team():
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    manager_name = request.form['manager_name']
    team_name = request.form['team_name']
    major = request.form['major']
    target = request.form['target']
    resume = request.form['resume']
    progress = request.form['progress']
    need = request.form['need']

    team = Team(manager_name=manager_name, team_name=team_name, major=major, creater_id=me.id, target=target,
                progress=progress,
                need=need, resume=resume)
    db.session.add(team)
    db.session.flush()
    db.session.commit()

    return jsonify(success=0, msg='成功添加队伍', team_id=team.id)


@team_mod.route('/team/upload', methods=['POST'])
def upload():
    if 'photo' in request.files and 'team_id' in request.form:
        pic = request.files['photo']
        if not pic.filename.startswith('https://www.chival.xyz'):  # 不是原来数据库里的文件
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))

            pic.filename = ran_str + pic.filename
            team_id = request.form.get("team_id")
            photos.save(pic)
            # print("$$$" + pic.filename + '%%%')
            db.session.add(TeamImage(team_id=team_id, url=pic.filename))
            db.session.commit()
            return jsonify(msg='upload file successfully', url=pic.filename)
    else:
        return jsonify(msg='upload file failed')
@team_mod.route('/all_teams')
def find_all_team():
    openid = request.values['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    teams = me.teams
    return jsonify(success=0, teams=[team.to_dict() for team in teams], msg='successfully get teams')


@team_mod.route('/random_teams')
def random_team():
    team_cnt = Team.query.count()
    indexset = set([random.randint(1, team_cnt) for i in range(10)])
    team_ids = db.session.query(Team.id).all()

    random_ids = list(team_ids[i - 1] for i in indexset)
    results = Team.query.filter(Team.id.in_(random_ids)).all()
    if results:
        return jsonify(success=0, teams=[result.to_dict() for result in results], msg='successfully get random teams')
    else:
        return jsonify(success=1, msg='get random team Error')

@team_mod.route('/get_team')
def get_team():
    openid = request.values['openid']  # GET方法的值在args里，post在form里，他们都在values里
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    team = Team.query.get(request.values['id'])
    return jsonify(success=0, team=team.to_dict(), msg='successfully get teams')


@team_mod.route('/delete_team', methods=['POST'])
def delete_team():
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    team_id = request.form['id']

    team = Team.query.filter_by(id=team_id).first()
    if not team:
        return jsonify(success=1, msg='team id is wrong')
    db.session.delete(team)
    db.session.commit()
    return jsonify(success=0, msg='delete successfully')


@team_mod.route('/update_team', methods=['POST'])
def update_team():
    pic_prefix = 'https://www.chival.xyz/pic/'
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    major = request.form['major']
    manager_name = request.form['manager_name']
    team_name = request.form['team_name']
    target = request.form['target']
    progress = request.form['progress']
    need = request.form['need']
    resume = request.form['resume']
    id = request.form['id']

    now_pic = request.form['now_pic']
    now_pic = json.loads(now_pic)
    print('now_pic is ' + str(now_pic))

    keep_pic = [item[len(pic_prefix):] for item in now_pic if item.startswith(pic_prefix)]
    print('keep_pic is ' + str(keep_pic))

    # 清除不在的图片
    delete_pic = TeamImage.query.filter(TeamImage.team_id == id).filter(TeamImage.url.notin_(keep_pic)).all()

    for pic in delete_pic:
        if os.path.exists(os.path.join(UPLOADED_PHOTO_DEST, pic.url)):
            os.remove(os.path.join(UPLOADED_PHOTO_DEST, pic.url))
    TeamImage.query.filter(TeamImage.team_id == id).filter(TeamImage.url.notin_(keep_pic)).delete(
        synchronize_session=False)
    db.session.commit()


    team = Team.query.filter_by(id=id).first()

    if not team:
        return jsonify(success=1, msg='team id is wrong')

    team.manager_name = manager_name
    team.team_name = team_name
    team.major = major
    team.target = target
    team.progress = progress
    team.need = need
    team.resume = resume

    db.session.commit()

    return jsonify(success=0, msg='成功修改队伍')
