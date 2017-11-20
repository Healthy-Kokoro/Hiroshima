# Standard library imports
from datetime import datetime

# First-party imports
from application import database

class BaseModel:
	def save(self):
		database.session.add(self)
		database.session.commit()

	def commit(self):
		database.session.commit()

class JsonModel(BaseModel):
	json_map = {}

	def to_json(self):
		json = {}

		for key, attribute in self.json_map.items():
			json[key] = getattr(self, attribute)

		return json

	@classmethod
	def from_json(cls, json):
		instance = cls()

		for key, attribute in cls.json_map.items():
			setattr(instance, attribute, json[key])

		return instance
