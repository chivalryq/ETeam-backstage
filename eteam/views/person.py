from flask import Blueprint, request, jsonify
from eteam import db, photos
from ..models import Person, PersonImage
from .user import find_user
from ..settings import UPLOADED_PHOTO_DEST
import random, string, os, json
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
    creater_id = me.id

    new_person = Person(name=name, major=major, resume=resume, creater_id=creater_id, \
                        post1=post1, post2=post2, tech=tech, art=art, software=software, \
                        expect_competition=expect_competition)

    db.session.add(new_person)
    db.session.commit()

    return jsonify(success=0, msg='create person successfully', id=new_person.id)


@person_mod.route('/random_people')
def random_people():
    person_cnt = Person.query.count()
    indexset = set([random.randint(1, person_cnt) for i in range(10)])
    person_ids = db.session.query(Person.id).all()

    random_ids = list(person_ids[i - 1] for i in indexset)
    results = Person.query.filter(Person.id.in_(random_ids)).all()
    if results:
        return jsonify(success=0, people=[result.to_dict() for result in results], msg='successfully get random people')
    else:
        return jsonify(success=1, msg='get random peroson Error')


@person_mod.route('/get_self')
def get_self():
    openid = request.values['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')

    person = me.person[0]
    if not person:
        return jsonify(success=1,msg="User doesn't have a person")

    return jsonify(success=0, person=person.to_dict(), msg='successfully get person')


@person_mod.route('/get_person')
def get_person():
    id = request.form['id']
    person = Person.query.get(id)
    if not person:
        return jsonify(success=1, msg="User doesn't have a person")

    return jsonify(success=0, person=person.to_dict(), msg='successfully get person')


@person_mod.route('/person/upload', methods=['POST'])
def upload():
    if 'photo' in request.files and 'team_id' in request.form:
        pic = request.files['photo']
        if not pic.filename.startswith('https://www.chival.xyz'):  # 不是原来数据库里的文件
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))

            pic.filename = ran_str + pic.filename
            person_id = request.form.get("person_id")
            photos.save(pic)
            # print("$$$" + pic.filename + '%%%')
            db.session.add(PersonImage(person_id=person_id, url=pic.filename))
            db.session.commit()
            return jsonify(msg='upload file successfully', url=pic.filename)
    else:
        return jsonify(msg='upload file failed')

@person_mod.route('/update_person', methods=['POST'])
def update_person():
    pic_prefix = 'https://www.chival.xyz/pic/'
    openid = request.form['openid']
    me = find_user(openid)
    if not me:
        return jsonify(success=1, msg='User not found or not login')
    try:
        id = request.form['id']
        person = Person.query.get(id)
        if not person:
            return jsonify(success=1, msg='person not found')
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

        now_pic = request.form['now_pic']
        now_pic = json.loads(now_pic)
        print('now_pic is ' + str(now_pic))

        keep_pic = [item[len(pic_prefix):] for item in now_pic if item.startswith(pic_prefix)]
        print('keep_pic is ' + str(keep_pic))

        # 清除不在的图片
        delete_pic = PersonImage.query.filter(PersonImage.person_id == id).filter(
            PersonImage.url.notin_(keep_pic)).all()

        for pic in delete_pic:
            if os.path.exists(os.path.join(UPLOADED_PHOTO_DEST, pic.url)):
                os.remove(os.path.join(UPLOADED_PHOTO_DEST, pic.url))
        PersonImage.query.filter(PersonImage.person_id == id).filter(PersonImage.url.notin_(keep_pic)).delete(
            synchronize_session=False)
        
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
