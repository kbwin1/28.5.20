from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):


    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'

    username = db.Column(db.Text, nullable=False, primary_key=True,)
    
    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False, unique=True)
    
    first_name = db.Column(db.Text, nullable=False)
    
    last_name = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
      
        hash = bcrypt.generate_password_hash(password)
      
        hash_utf8 = hash.decode("utf8")

        return cls(username=username, password=hash_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
          
            return user
        else:
            return False

class Feedback(db.Model):
         
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)
    
    username = db.Column(db.Text, db.ForeignKey('users.username',ondelete='CASCADE'))
    
    feed = db.relationship('User', backref="feedbacks")
    
    
    @classmethod
    def create(cls,title,content,username):
        return cls(title=title,content=content, username=username)