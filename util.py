"""
utility functions to share among models
"""
import json
import os
from datetime import datetime, date, time

from google.appengine.api import users
from google.appengine.ext import ndb
import google.appengine.ext

#pylint: disable=import-error
from protorpc import messages

import jrg.errors as errors

EPOCH = datetime(1970, 1, 1)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
    #pylint: disable=method-hidden

        if isinstance(o, ndb.Model):
            return o.to_dict()
        elif isinstance(o, (datetime, time)):
            return int((o - EPOCH).total_seconds() * 1000)
        elif isinstance(o, date):
            return str(o)
        elif isinstance(o, google.appengine.ext.ndb.key.Key):
            return o.id()
        elif isinstance(o, google.appengine.api.users.User):
            return {
                'email': o.email(),
                'nickname': o.nickname(),
                'user_id': o.user_id()
            }
        elif isinstance(o, messages.Enum):
            return o.name

        return super(JSONEncoder, self).default(o)

def to_json(ooo):
    return JSONEncoder(indent=2).encode(ooo)

def confirm_admin():
    if not users.is_current_user_admin():
        raise errors.NotAdmin

def is_prod():
    return os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/')

def is_dev():
    return not is_prod()

def confirm_dev():
    if not is_dev():
        raise errors.DevModeOnly

def ensure_key(maybe_key):
    if isinstance(maybe_key, google.appengine.ext.ndb.key.Key):
        return maybe_key

    # since this isn't a key it is probably a ndb model so it probably has a "key" attribute
    return maybe_key.key
