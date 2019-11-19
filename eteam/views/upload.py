from flask import Blueprint
from flask import request
from werkzeug.utils import secure_filename
import os
from .user import find_user
from ..utils import is_allowed_file
from ..settings import UPLOAD_FOLDER

upload=Blueprint('upload',__name__)
@upload.route('/upload_image')
def upload_image():
    file = request.files['file']
    openid = request.form['openid']
    me = find_user(openid)

    if file and  is_allowed_file(file.filenae):
        filename = secure_filename(file.filename)
        savepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(savepath)



