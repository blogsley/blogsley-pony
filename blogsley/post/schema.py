from collections import UserDict
import json

#class Schemata:

class Connection(UserDict): 
    def __init__(self, edges):
        self.edges = []

class PostConnection(UserDict):
    def __init__(self, objs):
        super().__init__()
        self.__typename = "PostConnection"
        self.edges = []
        self.pageInfo = None
        for obj in objs:
            self.edges.append(PostEdge(obj))


class PostEdge(UserDict):
    def __init__(self, obj):
        super().__init__()
        self.__typename = "PostEdge"
        self.cursor = ""
        self.node = PostNode(obj)


class PostNode(UserDict):
    def __init__(self, data):
        super().__init__()
        self.__typename = "Post"
        self.update(data)


if __name__ == "__main__":
    data = PostConnection([{"kind": "a"}, {"kind": "b"}, {"kind": "c"}])
    print(data)
    print(json.dumps(data.__dict__))
    
