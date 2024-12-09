import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True    

WTF_CSRF_ENABLED = True
SECRET_KEY = 'a-very-secret-secret'

# file upload configuration
UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')  # directory for uploaded files
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # alowed image extensions