from eteam import db
import datetime

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    openid=db.Column(db.String(255))
    nickname=db.Column(db.String(255))
    avater_url=db.Column(db.String(255))
    register_time= db.Column(db.DateTime, default=datetime.datetime.now)
    last_login_time= db.Column(db.DateTime, default=datetime.datetime.now)
    def __repr__(self):
        return "{0} {1} {2} {3} ".format(self.user_id,self.nickname,self.openid,self.last_login_time)

class Person(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    major=db.Column(db.Integer)
    img_url=db.relationship('PersonImage')

class Team(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    manager_name=db.Column(db.String(80))
    team_name=db.Column(db.String(60))
    img_url=db.relationship('TeamImage')

class TeamImage(db.Model):
    img_id=db.Column(db.Integer,primary_key=True)
    url=db.String(db.String(255))
    team_id=db.Column(db.Integer,db.ForeignKey("team.id"))

class PersonImage(db.Model):
    img_id = db.Column(db.Integer, primary_key=True)
    url = db.String(db.String(255))
    team_id = db.Column(db.Integer, db.ForeignKey("person.id"))