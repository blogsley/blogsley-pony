from hashlib import md5
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import UserMixin
#from blogsley.config import db, login
from pony import orm
from pony.orm import PrimaryKey, Set, Required, Optional
from blogsley.config import db
'''
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, 64, index=True, unique=True)
    first_name = Optional(str, 32)
    last_name = Required(str, 32)
    email = Required(str, 120, index=True, unique=True)
    password_hash = Required(str, 128)
    role = Required(str, 16)
    about_me = Required(str, 140)
    posts = Set('Post', reverse='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
