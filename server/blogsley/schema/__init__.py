from ariadne import make_executable_schema, QueryType, MutationType, SubscriptionType

import blogsley.config
from blogsley.config import type_defs

query = QueryType()
mutation = MutationType()
subscription = SubscriptionType()

def create_schema():
    # Create executable schema instance
    #config.schema = schema = make_executable_schema(type_defs, query, mutation, subscription)
    blogsley.config.schema = schema = make_executable_schema(type_defs, query, mutation, subscription)
    return schema
