from click import Group, group

import blogsley.application

class BlogsleyInfo:
    def __init__(self, create_app):
        self.app = app = create_app()

class BlogsleyGroup(Group):
    def __init__(self, name=None, commands=None, create_app=None, **attrs):
        super().__init__(name=None, commands=None, **attrs)
        self.create_app = create_app or blogsley.application.create_app

    def main(self, *args, **kwargs):
        obj = kwargs.get("obj")

        if obj is None:
            obj = BlogsleyInfo(create_app=self.create_app)

        kwargs["obj"] = obj
        kwargs.setdefault("auto_envvar_prefix", "BLOGSLEY")
        return super().main(*args, **kwargs)