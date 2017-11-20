# Standard library imports
from base64 import b64decode
from functools import wraps
from json import loads

# Third-party imports
from flask import current_app
from flask import request
from flask import jsonify

def make_json_response(results={}, status=200, message='SUCCESS', error_action=0):
	return jsonify({
		'cod': status,
		'msg': message,
		'rst': results,
		'eac': error_action
	})

def version_to_tuple(version):
	return tuple(map(int, version.split('.')))

def session_required(function):
	@wraps(function)
	def wrapper(*args, **kwargs):
		session = request.headers.get('X-Bs-Session')

		if session:
			session_version = None

			try:
				json = loads(b64decode(session))
				session_version = version_to_tuple(json['avs'])
			except:
				pass

			if session_version:
				version = version_to_tuple(current_app.config['HIROSHIMA_API_VERSION'])

				if session_version == version:
					return function(*args, **kwargs)
				elif session_version < version:
					return make_json_response(
						status=9999,
						message='Game requires update.',
						error_action=2
					)
				elif session_version > version:
					return make_json_response(
						status=9000,
						message='UNKNOWN_ERROR',
						error_action=0
					)
			else:
				return make_json_response(
					status=9015,
					message='MALFORMED_SESSION',
					error_action=1
				)
		else:
			return make_json_response(
				status=9014,
				message='SESSION_HEADER_REQUIRED',
				error_action=0
			)

	return wrapper
