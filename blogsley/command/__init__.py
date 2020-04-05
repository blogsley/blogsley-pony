import os
import click

import blogsley.config
from blogsley.app import create_app
from blogsley.command.group import CommandGroup
from blogsley.command.serve import serve as do_serve
from blogsley.command.populate import populate as do_populate
#TODO:Put these commands into seperate files and lazy load/deferred import
#from blogsley.command.populate import populate as do_populate

app = None

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['app'] = create_app()

@cli.command()
@click.pass_context
def init(ctx):
    do_populate()

@cli.command()
@click.pass_context
def run(ctx):
    print(ctx)
    print(ctx.obj)
    app = ctx.obj['app']
    os.environ["BLOGSLEY_ENV"] = "production"
    do_serve(app)

@cli.command()
@click.pass_context
def dev(ctx):
    app = ctx.obj['app']
    #os.environ["BLOGSLEY_ENV"] = "development"
    os.environ["BLOGSLEY_ENV"] = "debug"
    blogsley.config.debug = app.debug = True
    print(vars(ctx.obj))
    #ctx.obj._loaded_app.run(debug=True)
    blogsley.pywsgi.run(app)

@cli.command()
@click.pass_context
def populate(ctx):
    app = ctx.obj['app']
    do_populate(app)
