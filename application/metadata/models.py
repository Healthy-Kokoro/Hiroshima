# Standard library imports
from datetime import datetime

# First-party imports
from application import database
from application.models import JsonModel

class Metadata(database.Model, JsonModel):
	name = database.Column(database.String(128), primary_key=True)
	version = database.Column(database.Integer)

	def to_json(self):
		return {self.name: self.version}
