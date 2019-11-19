from flask import Blueprint,request
from eteam import db
from ..models import Person

mod=Blueprint("person",__name__)

@mod.route('/create_person',methods=['POST'])
def create_person():
    name=request.form['name']
    major=request.form['major']
    resume=request.form['resume']
    expect_competition=request.form['competition']


@mod.route('/update_person',method=['POST'])
def update_person():
    pass



