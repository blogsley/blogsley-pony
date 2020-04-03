from hashlib import md5
from pony import orm
from pony.orm import PrimaryKey, Set, Required, Optional

from blogsley.config import db
from blogsley.security import generate_password_hash, check_password_hash
'''
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
'''
class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, 64, index=True, unique=True)
    firstName = Optional(str, 32)
    lastName = Required(str, 32)
    email = Required(str, 120, index=True, unique=True)
    password_salt = Required(bytes) #32
    password_hash = Required(bytes) #32
    role = Required(str, 16)
    aboutMe = Required(str, 140)
    posts = Set('Post', reverse='author', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def full_name(self):
        return self.firstName + ' ' + self.lastName
    
    def set_password(self, password):
        salt, key = generate_password_hash(password)
        self.password_salt = salt
        self.password_hash = key

    def check_password(self, password):
        return check_password_hash(password, self.password_salt, self.password_hash)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
