#!/usr/bin/env python
import os
import subprocess

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from redis import Redis
from rq import Connection, Queue, Worker

from app import create_app, db
from app.models import Role, User
from app.wakkerdam.models import *
from config import Config

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Game=Game, Character=Character, Player=Player, Invite=Invite, ChatType=ChatType, Chat=Chat, Chatter=Chatter, Message=Message, ChatLog=ChatLog, Article=Article, Newspaper=Newspaper, Localization=Localization)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host="0.0.0.0"))


@manager.command
def delete_db():
    db.drop_all()
    print("Databases deleted")

@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all(bind=None)
    db.create_all(bind=None)
    db.session.commit()
    setup_dev()
    add_standard()

@manager.command
def create_localization():
    db.create_all(bind="localization")
    db.create_all(bind="localization")



@manager.option(
    '-n',
    '--number-users',
    default=10,
    type=int,
    help='Number of each model type to create',
    dest='number_users')
def add_fake_data(number_users):
    """
    Adds fake data to the database.
    """
    User.generate_fake(count=number_users)


@manager.command
def setup_dev():
    """Runs the set-up needed for local development."""
    
    return setup_general()


@manager.command
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


@manager.command
def prefill():
    """Prefills the tables ChatType, Character, ActionType, GroupType"""
    
    vill = regularVillager()
    db.session.add(vill)
    db.session.commit()

def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    Role.insert_roles()
    admin_query = Role.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL,
                avatar='steve',
                language='nl_NL')
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))
            return user


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    conn = Redis(
        host=app.config['RQ_DEFAULT_HOST'],
        port=app.config['RQ_DEFAULT_PORT'],
        db=0,
        password=app.config['RQ_DEFAULT_PASSWORD'])

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)

@manager.command
def add_standard():
    setup_general()
    admin = User.query.filter_by(id=1).first()
    user = User(confirmed=1, first_name='Daniël', last_name='Kuiper', email='mofferthond@gmail.com', password=Config.ADMIN_PASSWORD, role_id=1, avatar='steve', language="nl_NL")
    db.session.add(user)
    village_chat = ChatType(name='Dorpchat', opens='1100', closes='1900')
    db.session.add(village_chat)

    first_game = Game(name='Eerste spel', ongoing=1, startDate='2030-12-12', hostingUser=user, playerAmount=10)
    db.session.add(first_game)
    first_player = Player(user=admin, game=first_game, character=None)
    db.session.add(first_player)
    second_player = Player(user=user, game=first_game, character=None)
    db.session.add(second_player)
    first_chat = Chat(game=first_game, chatType=village_chat)
    db.session.add(first_chat)
    first_chatter = Chatter(player=first_player, chat=first_chat)
    db.session.add(first_chatter)
    second_chatter = Chatter(player=second_player, chat=first_chat)
    db.session.add(second_chatter)

    first_message = Message(chatter=first_chatter, text='Eerste bericht!', timestamp=1637415000)
    db.session.add(first_message)
    second_message = Message(chatter=second_chatter, text='Tweede bericht!', timestamp=1637415060)
    db.session.add(second_message)
    first_reply = Message(chatter=second_chatter, text='Eerste reactie?', replyTo=first_message, timestamp=1637415600)
    db.session.add(first_reply)


    first_newspaper = Newspaper(game=first_game, date="2021-12-23")
    db.session.add(first_newspaper)
    first_article = Article(text="Ik denk dat Admin Account wolf is.", publisher="de Ziener", playerCreated=first_player, newspaper=first_newspaper)
    db.session.add(first_article)
    second_article = Article(text="Ik weet dat Daniel Kuiper wolf is.", publisher="de Journalist", playerCreated=second_player, newspaper=first_newspaper)
    db.session.add(second_article)
    admin_article = Article(text="Admin Account is vannacht vermoord.", publisher=None, playerCreated=None, newspaper=first_newspaper)
    db.session.add(admin_article)

    db.session.commit()
    first_newspaper.setFormat(first_newspaper.createFormat())
    print('Added fake data')

if __name__ == '__main__':
    manager.run()
