import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, make_response, send_from_directory, request
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    prep_application = Flask(__name__)
    prep_application.debug = False
    # setup RotatingFileHandler with maxBytes set to 25MB
    rotating_log = RotatingFileHandler('voicemail_automator.log', maxBytes=25000000, backupCount=6)
    prep_application.logger.addHandler(rotating_log)
    rotating_log.setFormatter(logging.Formatter(fmt='[%(asctime)s] / %(levelname)s in %(module)s: %(message)s'))
    prep_application.logger.setLevel(logging.INFO)
    prep_application.secret_key = 'yhNmWEVXx7yLe2zikpBXshTDSHyeVNrB'
    prep_application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    prep_application.config['MAX_CONTENT_LENGTH'] = 256
    prep_application.config['PROGRAM_NAME'] = 'Voicemail Automator'
    prep_application.config['VERSION'] = 1.0
    prep_application.wsgi_app = ProxyFix(prep_application.wsgi_app, x_proto=1, x_host=1)
    return prep_application


application = create_app()
application.app_context().push()


@application.get('/')
def index():
    return make_response(jsonify({'message': 'hello'}), 200)


@application.get('5MwSoXWTuCGj777Ht25BdXN35aoyZczDHWhyLY4A')
def secret():
    if request.args:
        return make_response(jsonify({'message': 'secret!'}), 200)
