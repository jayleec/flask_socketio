import click

from sqlalchemy_utils import database_exists, create_database

from wilson.app import create_app
from wilson.extensions import db
from wilson.blueprints.user.models import User

from wilson.blueprints.api.models import Reply

# Create an app context for the database connection.
app = create_app()
db.app = app


@click.group()
def cli():
    """ Run PostgreSQL related tasks. """
    pass


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
def init(with_testdb):
    """
    Initialize the database.

    :param with_testdb: Create a test database
    :return: None
    """
    db.drop_all()
    db.create_all()

    if with_testdb:
        db_uri = '{0}_test'.format(app.config['SQLALCHEMY_DATABASE_URI'])

        if not database_exists(db_uri):
            create_database(db_uri)

    return None


@click.command()
def seed():
    if User.find_by_identity(app.config['SEED_ADMIN_EMAIL']) is not None:
        return None

    params = {
        'role': 'admin',
        'email': app.config['SEED_ADMIN_EMAIL'],
        'password': app.config['SEED_ADMIN_PASSWORD']
    }

    return User(**params).save()


@click.command()
def seed_wilson_test():
    r = Reply()
    r.id = 'init id'
    r.question_id = '1'
    r.user_id = 'initial message'
    r.feedback_id = 'initial message'
    r.message = 'initial message'

    return r


@click.command()
@click.option('--with-testdb/--no-with-testdb', default=False,
              help='Create a test db too?')
@click.pass_context
def reset(ctx, with_testdb):
    """
    Init and seed automatically.

    :param with_testdb: Create a test database
    :return: None
    """
    ctx.invoke(init, with_testdb=with_testdb)
    # ctx.invoke(seed)
    ctx.invoke(seed_wilson_test)

    return None


cli.add_command(init)
cli.add_command(seed)
cli.add_command(reset)
