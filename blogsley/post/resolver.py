import asyncio

from pony.orm import db_session
from blogsley.schema import query, mutation, subscription
from blogsley.post.schema import PostConnection, PostEdge, PostNode
from blogsley.post.hub import hub, PostSubscriber, PostEvent
from blogsley.post.entity import Post

# Queries

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

# Mutations

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

# Subscriptions

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