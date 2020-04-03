import json
import graphene
from graphene import relay
from graphql_relay import to_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from blogsley.config import db
from blogsley.models.users import User
from blogsley.models.blog import Post

from blogsley.jwt import encode_auth_token, decode_auth_token

class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )

class UserConnection(relay.Connection):
    class Meta:
        node = UserNode

class UserInput(graphene.InputObjectType):
    username = graphene.String()
    email = graphene.String()
    firstName = graphene.String()
    lastName = graphene.String()

class LoginInput(graphene.InputObjectType):
    username = graphene.String()
    password = graphene.String()

class CreateUser(graphene.Mutation):
    class Arguments:
        data = UserInput(required=True)

    id = graphene.ID()

    @staticmethod
    def mutate(self, info, data=None):
        print('CreateUser')
        user = User(
            username=data.username,
            email=data.email,
            firstName=data.firstName,
            lastName=data.lastName,
            # role='Reader',
            # about_me='I am a Reader'
        )
        # user.set_password(password)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        id = to_global_id(UserNode._meta.name, user.id)
        return CreateUser(id=id)

class UpdateUser(graphene.Mutation):
    class Arguments:
        _id = graphene.ID(required=True)
        data = UserInput(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, _id, data=None):
        print('UpdateUser')
        print(_id)
        user = graphene.Node.get_node_from_global_id(info, _id)
        print(user)
        user.username = data.username
        user.email = data.email
        user.save()
        ok = True

        return ok

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, id):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
        user = graphene.Node.get_node_from_global_id(info, id)
        print(user)
        db.session.delete(user)
        db.session.commit()
        ok = True

        return ok

class Mutation(graphene.ObjectType):
    login = Login.Field()
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

class Query(graphene.ObjectType):
    user = relay.Node.Field(UserNode)
    all_users = SQLAlchemyConnectionField(UserConnection)
