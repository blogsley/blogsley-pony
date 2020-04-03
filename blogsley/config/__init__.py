  
import os
import sys

from starlette.config import Config

basedir = os.getcwd()
#TODO: Use TOML
'''
from dotenv import load_dotenv
load_dotenv(os.path.join(basedir, '.env'))
'''
#So Jinja2 can find templates
sys.path.append(os.path.join(os.path.dirname(__file__), "./templates"))

# Globals
app = None
db = None
type_defs = None
login = None
share_folder = None
db_folder = None
static_folder = None
debug = True

# Read the schema
with open(os.path.join(basedir, 'schema.gql'), "r") as fh:
    type_defs = fh.read()

# Set Globals
pip_share_folder = os.path.join(sys.prefix, 'share/blogsley')
is_pip_install = os.path.isdir(pip_share_folder)

if is_pip_install:
    share_folder = pip_share_folder
else:
    share_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '../share/blogsley'))


project_share_folder = os.path.abspath('share/blogsley')
is_project = os.path.isdir(project_share_folder)

if is_project:
    db_folder = project_share_folder
else:
    db_folder = share_folder


static_folder = f'{share_folder}/static'

'''
if debug:
    if is_pip_install:
        raise Exception('You need to run this in the project root directory!')
else:
    pass
'''



env = {
    'MEDIA_ROOT': '/storage/media' if os.environ.get("DOKKU_APP_TYPE") else basedir + '/public/media',
    'SECRET_KEY': os.environ.get('SECRET_KEY') or 'you-will-never-guess',
    'DATABASE_URI': os.environ.get('DATABASE_URI') or os.path.join(db_folder, 'blogsley.db')
    }
environ = os.environ.copy()
environ.update(env)
config = Config(environ=environ)