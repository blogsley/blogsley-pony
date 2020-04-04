import asyncio

from pony.orm import db_session
from blogsley.schema import query, mutation, subscription
from blogsley.schema.schemata import Connection, Edge, Node
from blogsley.message import MessageHub, Subscriber, Event
from blogsley.post import Post


class PostConnection(Connection):
    def __init__(self, objs):
        super().__init__(objs, edge_class=PostEdge, node_class=PostNode)


class PostEdge(Edge):
    def __init__(self, obj, node_class):
        super().__init__(obj, PostNode)


class PostNode(Node):
    def __init__(self, objekt):
        super().__init__(objekt)

class PostEvent(Event):
    def __init__(self, id, kind):
        super().__init__(id, kind)
####
hub = MessageHub()

class PostSubscriber(Subscriber):
    def __init__(self, id):
        super().__init__()
        self.id = id

    async def send(self, msg):
        print('put in queue')
        if msg.id != self.id:
            return
        await self.queue.put(msg)
####
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
    event = PostEvent(id, 'update')
    #await queue.put(event)
    await hub.send(event)

@subscription.source("postEvents")
async def events_generator(obj, info, id=None):
    print('events_generator:begin')
    subscriber = PostSubscriber(id)
    hub.subscribe(subscriber)
    while subscriber.active:
        #event = await queue.get()
        event = await subscriber.receive()
        print('events_resolver:while')
        print(event)
        yield event

@subscription.field("postEvents")
def events_resolver(event, info, id=None):
    print('events_resolver')
    print(event)
    return event