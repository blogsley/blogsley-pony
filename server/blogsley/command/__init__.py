import os
import click

import blogsley.config
from blogsley.application import create_app
from blogsley.command.group import BlogsleyGroup, BlogsleyInfo
from blogsley.command.serve import serve as do_serve
from blogsley.command.develop import develop as do_develop
from blogsley.command.populate import populate as do_populate
#TODO:Put these commands into seperate files and lazy load/deferred import
#from blogsley.command.populate import populate as do_populate

app = None

@click.group(cls=BlogsleyGroup)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(BlogsleyInfo)

@cli.command()
@click.pass_context
def init(ctx):
    do_populate()

@cli.command()
@click.pass_context
def run(ctx):
    app = ctx.obj.app
    os.environ["BLOGSLEY_ENV"] = "production"
    do_serve(app)

@cli.command()
@click.pass_context
def dev(ctx):
    app = ctx.obj.app
    #os.environ["BLOGSLEY_ENV"] = "development"
    os.environ["BLOGSLEY_ENV"] = "debug"
    blogsley.config.debug = app.debug = True
    do_develop(app)

@cli.command()
@click.pass_context
def populate(ctx):
    app = ctx.obj.app
    do_populate(app)
