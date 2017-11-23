# Standard library imports
from os import getenv

# Third-party imports
from flask_script import Manager

# First-party imports
from application import database
from application.init import models
from application.metadata import models
from updater import Updater
from wgsi import application

manager = Manager(application, with_default_commands=False)

@manager.command
def create_database():
	database.create_all()
	database.session.commit()

@manager.command
def update():
	updater = Updater()
	updater.update_asset_bundles()
	updater.update_metadata()

@manager.command
def setup():
	try:
		create_database()
	except:
		print('Failed to setup database!')

	try:
		update()
	except:
		print('Failed to setup updates!')

if __name__ == '__main__':
	manager.run()
