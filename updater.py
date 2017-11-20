# Standard library imports
from base64 import b64encode
from json import dumps

# Third-party imports
from flask import current_app
from requests import Session
from requests.exceptions import Timeout

# First-party imports
from application.init.models import AssetBundle

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

	def update_asset_bundles(self):
		print('Attempting to update the asset bundles...')

		for attempt in range(3):
			print('Attempting to reach the server...')

			try:
				json = self.session.get('{}/api/init'.format(current_app.config['HIROSHIMA_UPDATER_API_URI'])).json()

				if json.get('cod') == 200:
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
							print('{} asset bundle was obsolete ({} < {}).'.format(name, asset_bundle.version, version))
						else:
							print('{} asset bundle is current.'.format(name))
					print('Updated the asset bundles.')
					
					return True
				else:
					print('The server refused to be reached (Reason: {})!'.format(json.get('msg')))
			except Timeout:
				print('The server could not be reached!')

		print('Failed to update the asset bundles!')
