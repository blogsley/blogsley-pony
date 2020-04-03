from pony.orm import db_session
from blogsley.schema import query, mutation
from blogsley.config import db
from blogsley.user import User
from blogsley.auth.jwt import encode_auth_token, decode_auth_token
#
# Mutations
#

#login(data: LoginInput!): LogIn!
@mutation.field("login")
@db_session
def resolve_login(_, info, data):
    print('Login')
    print(data)
    request = info.context["request"]
    username=data['username']
    password=data['password']

    if not username:
        raise Exception('Username missing!')
    if not password:
        raise Exception('Password missing!')

    user = User.select(lambda p:p.username == username).first()
    if user is None or not user.check_password(password):
        raise Exception('No such user or invalid password!')

    # Identity can be any data that is json serializable
    access_token = encode_auth_token(sub=username, id=user.id)
    print(access_token)
    # token = json.dumps({"token": access_token.decode('utf-8')})
    token = access_token.decode('utf-8')
    print(token)
    return { 'token': token }
