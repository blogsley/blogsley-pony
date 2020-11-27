class IsAuthorizedDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve or default_field_resolver
        def resolve_is_authorized(obj, info, **kwargs):
            user = info.context.get('user')
            if user is None:
                raise GraphQLError(message="Not authenticated.")
            roles = self.args.get("roles")
            if roles is not None:
                if user.role not in roles:
                    raise GraphQLError(message="Not authorized.")
            result = original_resolver(obj, info, **kwargs)
            return result
        field.resolve = resolve_is_authorized
        return field

# Put in Schema!
directive @isAuthenticated on FIELD_DEFINITION
directive @isAuthorized(roles: [Role]) on FIELD_DEFINITION