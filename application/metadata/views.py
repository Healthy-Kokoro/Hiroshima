# Third-party imports
from flask import Blueprint
from flask import current_app

# First-party imports
from application.helpers import session_required
from application.helpers import make_json_response
from .models import Metadata

blueprint = Blueprint('metadata', __name__, url_prefix='/api/metaData')

@blueprint.route('/version/')
@session_required
def get_metadata_versions():
	metadata_versions = {}

	for metadata in Metadata.query.all():
		metadata_versions.update(metadata.to_json())

	return make_json_response(metadata_versions)
