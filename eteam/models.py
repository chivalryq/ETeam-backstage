from eteam import db
import datetime

class User(db.Model):
    __tablename__='user'#默认生成的就是这个，但是这里显示的指定是为了添加外键
    id=db.Column(db.Integer, primary_key=True)
    openid=db.Column(db.String(255))
    nickname=db.Column(db.String(255))
    avater_url=db.Column(db.String(255))
    register_time= db.Column(db.DateTime, default=datetime.datetime.now)
    last_login_time= db.Column(db.DateTime, default=datetime.datetime.now)

    teams=db.relationship('Team')
    person=db.relationship('Person')
    def __repr__(self):
        return "{0} {1} {2} {3} ".format(self.id,self.nickname,self.openid,self.last_login_time)

class Person(db.Model):
    __tablename__='person'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    major=db.Column(db.Integer)
    resume=db.Column(db.Text)
    expect_competition=db.Column(db.String(50))
    img_url=db.relationship('PersonImage')

    creater_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Team(db.Model):
    __tablename__ = 'team'
    id=db.Column(db.Integer,primary_key=True)

    manager_name=db.Column(db.String(80))
    major = db.Column(db.String(10))  # 负责人专业
    target=db.Column(db.String(20))#比赛
    resume = db.Column(db.Text)  # 队伍简介
    progress = db.Column(db.Text)  # 项目进度
    need = db.Column(db.String(20))  #人员需求

    img_url=db.relationship('TeamImage')
    creater_id=db.Column(db.Integer,db.ForeignKey('user.id'))

class TeamImage(db.Model):
    __tablename__ = 'team_image'
    img_id=db.Column(db.Integer,primary_key=True)
    url=db.String(db.String(255))
    team_id=db.Column(db.Integer,db.ForeignKey("team.id"))

class PersonImage(db.Model):
    __tablename__ = 'person_image'
    img_id = db.Column(db.Integer, primary_key=True)
    url = db.String(db.String(255))
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))