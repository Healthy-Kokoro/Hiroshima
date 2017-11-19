# Third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

configurations = {
	'development': 'configurations.DevelopmentConfiguration',
	'testing': 'configurations.TestingConfiguration',
	'staging': 'configurations.StagingConfiguration',
	'production': 'configurations.ProductionConfiguration'
}

database = SQLAlchemy()

def create_application(configuration):
	application = Flask(__name__, instance_relative_config=True)
	application.config.from_object(configurations[configuration])
	application.config.from_pyfile('configuration.py', silent=True)
	database.init_app(application)

	return application
