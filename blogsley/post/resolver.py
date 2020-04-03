from blogsley.schema import query
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
