from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

from ariadne.asgi import GraphQL

from blogsley.schema import create_schema
from blogsley.db import load_db
# Pull in our models
import blogsley.model
# Pull in our resolvers
import blogsley.resolver

app = None

def create_app(debug=True):
    global app
    if app:
        return app
    app = Starlette(debug=debug)
    #app = FastAPI(debug=debug)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    db = load_db()
    schema = create_schema()
    app.mount("/graphql", GraphQL(schema, debug=debug))
    return app