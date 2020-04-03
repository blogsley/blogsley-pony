from blogsley.schema import query, mutation


@query.field("allUsers")
def resolve_users(*_):
    session = Session()
    todos = session.query(User).all()

#
# Mutations
#
