import os
db_account='eteam'
db_password='@Aa123456'
db_server='localhost:3306'
SQLALCHEMY_DATABASE_URI = 'mysql://'+db_account+':'+db_password+'@'+db_server+'/testdb1' #数据库设置

SECRET_KEY='secret_key'
SQLALCHEMY_TRACK_MODIFICATIONS=True
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
STATIC_DIR_PATH=r"/root/static_dir/static"#静态文件目录
UPLOAD_FOLDER=os.path.join(STATIC_DIR_PATH,'img')#上传文件目录
