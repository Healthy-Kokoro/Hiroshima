# Standard library imports
from os import getenv

# Third-party imports
from flask_script import Manager

# First-party imports
from application import database
from wgsi import application

manager = Manager(application, with_default_commands=False)

@manager.command
def create_database():
	database.create_all()
	database.session.commit()

if __name__ == '__main__':
	manager.run()
