# Third-party imports
from flask import Blueprint
from flask import current_app

# First-party imports
from application.helpers import session_required
from application.helpers import make_json_response
from .models import AssetBundle

blueprint = Blueprint('init', __name__, url_prefix='/api/init')

@blueprint.route('/')
@session_required
def get_initialization_data():
	return make_json_response({
		'latestAssetBundles': [asset_bundle.to_json() for asset_bundle in AssetBundle.query.all()],
		'assetDownloadUrlAws': current_app.config['HIROSHIMA_ASSET_URI'],
		'assetDownloadUrlBase': current_app.config['HIROSHIMA_ASSET_URI'],
		'updateRecommended': False
	})
