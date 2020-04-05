from click import Group, group

from blogsley.app import create_app

class CommandInfo:
    def __init__(self):
        app = create_app()
        self.app = app

class CommandGroup(Group):
    def __init__(self, name=None, commands=None, **attrs):
        context_settings = { 'obj': CommandInfo() }
        super().__init__(name=None, commands=None, context_settings=context_settings, **attrs)
