from flask import Blueprint,request,jsonify
from eteam import db
from ..models import Team
from .user import find_user
team_mod=Blueprint("team", __name__)

@team_mod.route('/create_team', method=['POST'])
def create_team():
    openid=request.form['openid']
    me=find_user(openid)
    if not me:
        return jsonify(success=1,msg='User not found or not login')

    team_name=request.form['team_name']
    manager_name=request.form['manager_name']
    target=request.form['target']
    progress=request.form['progress']
    need=request.form['need']
    resume = request.form['resume']

    db.session.add(
        Team(manager_name=manager_name, creater_id=me.id, team_name=team_name, target=target, progress=progress,
             need=need, resume=resume))
    db.session.commit()

    return jsonify(success=0,msg='成功添加队伍')

@team_mod.route('/all_teams')
def find_all_team():
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    teams=me.teams
    return jsonify(success=0,teams=teams,msg='successfully get teams')

@team_mod.route('/delete_team', method=['POST'])
def delete_team():
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    team_id=request.form['id']

    team=Team.query.filter_by(id=team_id).first()
    if not team:
        return jsonify(success=1, msg='team id is wrong')
    db.session.delete(team)
    db.session.commit()
    return jsonify(success=0, msg='delete successfully')


@team_mod.route('/update_team', method=['POST'])
def update_team():
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    team_name = request.form['team_name']
    manager_name = request.form['manager_name']
    target = request.form['target']
    progress = request.form['progress']
    need = request.form['need']
    resume = request.form['resume']


    team=Team.query.filter_by(id=id)

    if not team:
        return jsonify(success=1, msg='team id is wrong')
    team.team_name=team_name
    team.manager_name=manager_name
    team.target=target
    team.progress=progress
    team.need=need
    team.resume = resume

    db.session.commit()

    return jsonify(success=0, msg='成功修改队伍')
