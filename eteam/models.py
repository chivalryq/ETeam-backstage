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
    major = db.Column(db.String(10))
    resume=db.Column(db.Text)

    post1 = db.Column(db.String(10))  # 第一志愿
    post2 = db.Column(db.String(10))  # 第二志愿
    tech = db.Column(db.String(30))
    art = db.Column(db.String(30))
    software = db.Column(db.String(30))

    expect_competition = db.Column(db.String(10))

    img_url=db.relationship('PersonImage')

    creater_id = db.Column(db.Integer, db.ForeignKey('user.id'))  #外键

    def to_dict(self):
        model_dict = dict(self.__dict__)
        model_dict['img_url'] = [item.to_dict() for item in self.img_url]
        del model_dict['_sa_instance_state']
        return model_dict

    db.to_dict = to_dict  # 注意:这个跟使用SQLAlchemy的有区别

    # def todict(self):
    #     return dict(id=self.id,name=self.name,major=self.major,resume=self.resume,post1=self.post1,post2=self.post2,\
    #                 tech=self.tech,art=self.art,software=self.software,expect_competition=self.expect_competition,\
    #                 img_url=[item.todict() for item in self.img_url])
class Team(db.Model):
    __tablename__ = 'team'
    id=db.Column(db.Integer,primary_key=True)

    manager_name=db.Column(db.String(80))
    team_name = db.Column(db.String(80))
    major = db.Column(db.String(10))  # 负责人专业
    target = db.Column(db.String(10))  # 比赛

    resume = db.Column(db.Text)  # 队伍简介
    progress = db.Column(db.Text)  # 项目进度
    need = db.Column(db.String(30))  #人员需求

    img_url=db.relationship('TeamImage')
    creater_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def to_dict(self):
        model_dict = dict(self.__dict__)
        model_dict['img_url'] = [item.to_dict() for item in self.img_url]
        del model_dict['_sa_instance_state']
        return model_dict

    db.to_dict = to_dict  # 注意:这个跟使用SQLAlchemy的有区别
    # def todict(self):
    #     return dict(id=self.id,manager_name=self.manager_name,team_name=self.team_name,major=self.major,\
    #                 target=self.target,resume=self.resume,progress=self.progress,need=self.need, \
    #                 img_url=[item.todict() for item in self.img_url])
class TeamImage(db.Model):
    __tablename__ = 'team_image'
    img_id=db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(255))
    team_id=db.Column(db.Integer,db.ForeignKey("team.id"))

    def to_dict(self):
        return dict(img_url=self.url)

    db.to_dict = to_dict  # 注意:这个跟使用SQLAlchemy的有区别
    # def todict(self):
    #     return dict(img_id=self.img_id,url=str(self.url),team_id=self.team_id)
class PersonImage(db.Model):
    __tablename__ = 'person_image'
    img_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))

    def to_dict(self):
        return dict(img_url=self.url)

    db.to_dict = to_dict  # 注意:这个跟使用SQLAlchemy的有区别
    # def todict(self):
    #     return dict(img_id=self.img_id,url=str(self.url),person_id=self.person_id)
