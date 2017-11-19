# Standard library imports
from os import getenv

# First-party imports
from application import create_application

application = create_application(getenv('ENVIRONMENT', default='production'))
application.app_context().push()

if __name__ == '__main__':
	application.run(port=80)
