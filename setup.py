"""
utility functions to share among models
"""
import traceback
import logging

#pylint: disable=import-error
from werkzeug.exceptions import default_exceptions
import jrg

def setup(app):
    @app.errorhandler(Exception)
    def handle_invalid_usage(error):
        rv = error.__dict__
        rv['type'] = str(type(error).__name__)
        rv['stack'] = traceback.format_exc().split('\n')

        logging.error('invalid usage %s', rv['type'])
        logging.error('invalid usage\n%s', rv['stack'])

        return jrg.util.to_json(rv), 499

    # got this extra bit from https://stackoverflow.com/a/29332131
    # seems as though default HTML exceptions are handled differently
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_invalid_usage)
