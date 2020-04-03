from collections import UserDict
import json
from pony.orm import db_session
from blogsley.post import Post

class Schemata:
    def __init__(self):
        self.typename = self.__class__.__name__
    def wire(self):
        return {}

class Connection(Schemata): 
    def __init__(self, objs, edge_class, node_class):
        super().__init__()
        self.edges = []
        self.pageInfo = None
        for obj in objs:
            self.edges.append(edge_class(obj, node_class))

    def wire(self):
        result = {
            '__typename': self.typename,
            'edges': [edge.wire() for edge in self.edges],
            'pageInfo': self.pageInfo
            }
        return result

class Edge(Schemata):
    def __init__(self, obj, node_class):
        super().__init__()
        self.cursor = ""
        self.node = node_class(obj)

    def wire(self):
        result = {
            '__typename': self.typename,
            'cursor': self.cursor,
            'node': self.node.wire()
        }
        return result

class Node(Schemata):
    def __init__(self, objekt):
        super().__init__()
        self.objekt = objekt

    def wire(self):
        result = self.objekt.to_dict()
        result['__typename'] = self.typename,
        return result

class PostConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=PostEdge, node_class=PostNode)


class PostEdge(Edge):
    def __init__(self, obj, node_class):
        super().__init__(obj, PostNode)


class PostNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

@db_session
def test():
    #posts = Post.select()
    posts = [p for p in Post.select()]
    for p in posts:
        print(p.id, p.author.username, p.body)

    connection = PostConnection(posts)
    print(connection.wire())

if __name__ == "__main__":
    test()    
