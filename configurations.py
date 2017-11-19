# Standard library imports
from os import getenv

class Configuration:
	DEBUG = False
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfiguration(Configuration):
	DEBUG = True
	JSONIFY_PRETTYPRINT_REGULAR = True
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///development.db')

class TestingConfiguration(Configuration):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///testing.db')

class StagingConfiguration(Configuration):
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///staging.db')

class ProductionConfiguration(Configuration):
	SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL', default='sqlite:///production.db')
