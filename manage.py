# Standard library imports
from os import getenv

# Third-party imports
from flask_script import Manager

# First-party imports
from application import database
from application.init import models
from updater import Updater
from wgsi import application

manager = Manager(application, with_default_commands=False)

@manager.command
def create_database():
	database.create_all()
	database.session.commit()

@manager.command
def update_asset_bundles():
	updater = Updater()
	updater.update_asset_bundles()

if __name__ == '__main__':
	manager.run()
