from datetime import datetime
from slugify import slugify
#from bs4 import BeautifulSoup

from pony import orm
from pony.orm import PrimaryKey, Set, Required, Optional

from blogsley.config import db

class Post(db.Entity):
    id = PrimaryKey(int, auto=True)
    status = Required(str, 16, default='draft')
    title = Required(str, 256)
    slug = Optional(str, 256)
    model = Required(str)
    cover = Optional(str, 256)
    body = Required(str)
    timestamp = Required(datetime, index=True, default=datetime.utcnow())
    author = Set('User', lazy=True)
    # tags

    def __init__(self, *args, **kwargs):
        
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))

        super().__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        super(Post, self).__setattr__(key, value)
        if key == 'title':
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post {}>'.format(self.body)

'''
@event.listens_for(Post.body, 'set', retval=True)
def validate_body(target, value, oldvalue, initiator):
    return BeautifulSoup(value, 'html.parser').prettify()
'''