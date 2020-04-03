import asyncio

from pony.orm import db_session
from blogsley.schema import query, mutation, subscription
from blogsley.schema.schemata import Connection, Edge, Node
from blogsley.post import Post

queue = asyncio.Queue()
"""
  allPosts(
    # The number of items to return per page.
    _size: Int
    # The pagination cursor.
    _cursor: String
  ): PostPage!
"""
class PostConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=PostEdge, node_class=PostNode)


class PostEdge(Edge):
    def __init__(self, obj, node_class):
        super().__init__(obj, PostNode)


class PostNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

class Event:
    def __init__(self, kind='default', ok=True):
        self.kind = kind
        self.ok = ok


class PostEvent(Event):
    def __init__(self, kind):
        super().__init__(kind)

@query.field("post")
@db_session
def resolve_post(*_, id):
  return Post[id]

@query.field("allPosts")
@db_session
def resolve_all_posts(*_):
    #posts = Post.select()
    posts = [p for p in Post.select()]
    connection = PostConnection(posts)
    result = connection.wire()
    #print(result)
    return result

@mutation.field("updatePost")
@db_session
async def resolve_update_post(_, info, id, data):
    print('post:update')
    #print(data)
    request = info.context["request"]
    Post[id].set(**data)
    event = PostEvent('update')
    await queue.put(event)

'''
@subscription.source("postEvents")
async def post_generator(obj, info):
    yield { kind: 'waiting' }
    for i in range(5):
        await asyncio.sleep(1)
        yield i


@subscription.field("postEvents")
def post_resolver(count, info):
    return count + 1
'''

#
#
'''
@query.field("eventPost")
async def resolve_eventPost(obj, info, data_from_post):
    await queue.put(data_from_post)
    return 'It worked!'
'''
#
#
@subscription.source("postEvents")
async def events_generator(obj, info, id=None):
    print('events_generator:begin')
    print(obj)

    while True:
        event = await queue.get()
        print('events_resolver:while')
        print(event)
        yield event
#
#
@subscription.field("postEvents")
def events_resolver(event, info, id=None):
    print('events_resolver')
    print(event)
    return event