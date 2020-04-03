from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from starlette.applications import Starlette
'''
type_defs = """
    type Query {
        hello: String!
    }
"""
'''

with open("schema.graphql", "r") as fh:
    type_defs = fh.read()

query = QueryType()


"""
  allPosts(
    # The number of items to return per page.
    _size: Int
    # The pagination cursor.
    _cursor: String
  ): PostPage!
"""
@query.field("allPosts")
def resolve_hello(*_):
    return "Hello world!"


# Create executable schema instance
schema = make_executable_schema(type_defs, query)

app = Starlette(debug=True)
app.mount("/graphql", GraphQL(schema, debug=True))