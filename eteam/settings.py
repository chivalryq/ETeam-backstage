import os
from flask_uploads import IMAGES
db_account='eteam'
db_password='@Aa123456'
db_server='localhost:3306'
SQLALCHEMY_DATABASE_URI = 'mysql://'+db_account+':'+db_password+'@'+db_server+'/testdb1' #数据库设置

UPLOADED_PHOTO_DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pic')
UPLOADED_PHOTO_ALLOW = IMAGES

SECRET_KEY='secret_key'
SQLALCHEMY_TRACK_MODIFICATIONS=True
