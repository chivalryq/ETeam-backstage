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
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')
    try:
        id = request.form['id']
        person = Person.query.get(id)

        name = request.form['name']
        major = request.form['major']
        resume = request.form['resume']
        post1 = request.form['post1']
        post2 = request.form['post2']
        tech = request.form['tech']
        art = request.form['art']
        software = request.form['software']
        expect_competition = request.form['expect_competition']

        person.name = name
        person.major = major
        person.resume = resume
        person.post1 = post1
        person.post2 = post2
        person.tech = tech
        person.art = art
        person.software = software
        person.expect_competition = expect_competition

        db.session.commit()
    except:
        return jsonify(success=1, msg='Update person failed')

    return jsonify(success=0, msg='Update person successfully')


@person_mod.route('/delete_person', methods=['POST'])
def delete_person():
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')
    try:
        id = request.form['id']
        person = Person.query.get(id)

        db.session.delete(person)
        db.session.commit()

    except:
        return jsonify(success=1, msg='Delete person failed')

    return jsonify(success=0, msg='Delete person successfully')
