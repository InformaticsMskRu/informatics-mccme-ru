import sys
from pyramid.paster import get_app
sys.path.append('/var/pynformatics3/dev')
application = get_app(
  '/var/pynformatics3/dev/development.ini', 'main')