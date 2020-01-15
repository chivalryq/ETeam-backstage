from flask import Blueprint, request, jsonify
from eteam import db
from ..models import Person
from .user import find_user

person_mod=Blueprint("person", __name__)

@person_mod.route('/create_person', methods=['POST'])
def create_person():

    openid=request.form['openid']
    me=find_user(openid)
    if not me:
        return jsonify(success=1,msg='User not found or not login')

    name=request.form['name']
    major=request.form['major']
    resume=request.form['resume']

    post1 = request.form['post1']
    post2 = request.form['post2']
    tech = request.form['tech']
    art = request.form['art']
    software = request.form['software']

    expect_competition=request.form['expect_competition']

    db.session.add(Person(name=name, major=major, resume=resume, \
                          post1=post1, post2=post2, tech=tech, art=art, software=software, \
                          expect_competition=expect_competition))
    db.session.commit()
    return jsonify(success=0,msg='create person successfully')

@person_mod.route('/get_person')
def get_person():

    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    person=me.person
    if not person:
        return jsonify(success=1,msg="User doesn't have a person")

    return jsonify(success=0,person=person,msg='successfully get person')


@person_mod.route('/update_person', methods=['POST'])
def update_person():
    pass



