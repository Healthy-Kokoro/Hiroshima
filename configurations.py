# Standard library imports
from os import getenv

class Configuration:
	DEBUG = False
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	HIROSHIMA_API_VERSION = getenv('API_VERSION', default='3.6.00')
	HIROSHIMA_ASSET_URI = getenv('ASSET_URI', default='http://127.0.0.1/Real/ANDROID')

	HIROSHIMA_UPDATER_API_URI = getenv('UPDATER_API_URI', default='http://127.0.0.1')
	HIROSHIMA_UPDATER_API_VERSION = getenv('UPDATER_API_VERSION', default='3.6.00')

class DevelopmentConfiguration(Configuration):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///development.db')

class TestingConfiguration(Configuration):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///testing.db')

class StagingConfiguration(Configuration):
	JSONIFY_PRETTYPRINT_REGULAR = False
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///staging.db')

class ProductionConfiguration(Configuration):
	JSONIFY_PRETTYPRINT_REGULAR = False
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///production.db')
