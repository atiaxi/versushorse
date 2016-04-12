import sys
from os import environ
sys.path.append('/var/www/vhosts/versushorse/')

from index import app as _application


def application(req_environ, start_response):
    # Have to do this here because WSGI and apache environments are
    # apparently two different things for some reason.
    environ['VERSUSHORSE_CONFIG'] = req_environ['VERSUSHORSE_CONFIG']
    if environ['VERSUSHORSE_CONFIG']:
        _application.config.from_envvar('VERSUSHORSE_CONFIG')
    return _application(req_environ, start_response)
