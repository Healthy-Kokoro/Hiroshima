# Standard library imports
from base64 import b64encode
from json import dumps

# Third-party imports
from flask import current_app
from requests import Session
from requests.exceptions import Timeout

# First-party imports
from application.init.models import AssetBundle
from application.metadata.models import Metadata

class Updater():
	def __init__(self):
		self.session = Session()
		self.session.headers.update({
			'X-Bs-Session': b64encode(dumps({
				'snm': 0,
				'otp': 1,
				'ovs': '8.0.0',
				'avs': current_app.config['HIROSHIMA_UPDATER_API_VERSION'],
				'gst': False,
				'snk': None,
				'dlc': 'en',
				'alc': 'en',
				'mkt': 2
			}).encode('UTF-8'))
		})

	def update(self, route):
		for attempt in range(3):
			print('Attempting to fetch updates from {}...'.format(route))

			try:
				json = self.session.get('{}{}'.format(current_app.config['HIROSHIMA_UPDATER_API_URI'], route), timeout=10).json()

				if json.get('cod') == 200:
					return json
				else:
					print('The server refused to be reached! Reason: {}'.format(json.get('msg')))
			except Timeout:
				print('The server could not be reached!')

		print('Failed to fetch updates from {}!'.format(route))

	def update_asset_bundles(self):
		json = self.update('/api/init')

		if json:
			for asset_bundle_metadata in json['rst']['latestAssetBundles']:
				name = asset_bundle_metadata['abn']
				version = asset_bundle_metadata['vsn']
				asset_bundle = AssetBundle.query.get(name)

				if asset_bundle is None:
					AssetBundle(name=name, version=version).save()
					print('{} asset bundle was created.'.format(name))
				elif asset_bundle.version < version:
					asset_bundle.version = version
					asset_bundle.commit()
					print('{} asset bundle was updated.'.format(name))
				else:
					print('{} asset bundle is current.'.format(name))
			print('Successfully updated asset bundles.')

			return True
		else:
			print('Failed to update asset bundles!')

	def update_metadata(self):
		json = self.update('/api/metaData/version')

		if json:
			for name, version in json['rst'].items():
				metadata = Metadata.query.get(name)

				if metadata is None:
					Metadata(name=name, version=version).save()
					print('{} metadata was created.'.format(name))
				elif metadata.version < version:
					metadata.version = version
					metadata.commit()
					print('{} metadata was updated.'.format(name))
				else:
					print('{} metadata is current.'.format(name))
			print('Successfully updated metadata.')

			return True
		else:
			print('Failed to update metadata!')
