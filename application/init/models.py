# Standard library imports
from datetime import datetime

# First-party imports
from application import database
from application.models import JsonModel

class AssetBundle(database.Model, JsonModel):
	name = database.Column(database.String(128), primary_key=True)
	version = database.Column(database.Integer)
	created_at = database.Column(database.DateTime, default=datetime.utcnow)
	updated_at = database.Column(database.DateTime, default=datetime.utcnow)

	json_map = {
		'abn': 'name',
		'vsn': 'version'
	}

	def __init__(self, name, version):
		self.name = name
		self.version = version

	def commit(self):
		self.updated_at = datetime.utcnow()
		super().commit()
