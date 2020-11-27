from pony.orm import db_session
from blogsley.schema import query
from blogsley.schema.schemata import Connection, Edge, Node
from blogsley.user import User



class UserConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=UserEdge, node_class=UserNode)


class UserEdge(Edge):
    def __init__(self, obj, node_class):
        super().__init__(obj, UserNode)


class UserNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

@query.field("user")
@db_session
def resolve_user(*_, id):
  return User[id]

@query.field("allUsers")
@db_session
def resolve_all_users(*_):
    #users = User.select()
    users = [p for p in User.select()]
    connection = UserConnection(users)
    result = connection.wire()
    #print(result)
    return result
    