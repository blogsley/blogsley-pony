import os
import click

import blogsley.config
from blogsley.command.populate import populate as do_populate
#TODO:Put these commands into seperate files and lazy load/deferred import
#from blogsley.command.populate import populate as do_populate


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    os.environ["FLASK_RUN_FROM_CLI"] = "false"
    #os.environ["FLASK_APP"] = "blogsley:create_app"
    #os.environ["FLASK_APP"] = "blogsley"

@cli.command()
@click.pass_context
def init(ctx):
    flask_migrate.init()
    flask_migrate.migrate()
    flask_migrate.upgrade()
    do_populate()

@cli.command()
@click.pass_context
def run(ctx):
    app = ctx.obj._loaded_app
    os.environ["FLASK_ENV"] = "production"
    print(vars(ctx.obj))
    #ctx.obj._loaded_app.run()
    blogsley.pywsgi.run(app)

@cli.command()
@click.pass_context
def dev(ctx):
    app = ctx.obj._loaded_app
    #os.environ["FLASK_ENV"] = "development"
    os.environ["FLASK_ENV"] = "debug"
    blogsley.config.debug = app.debug = True
    print(vars(ctx.obj))
    #ctx.obj._loaded_app.run(debug=True)
    blogsley.pywsgi.run(app)

@cli.command()
@click.pass_context
def populate(ctx):
    do_populate()
