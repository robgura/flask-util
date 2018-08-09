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

import errors

EPOCH = datetime(1970, 1, 1)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
    #pylint: disable=method-hidden

        if isinstance(o, ndb.Model):
            return o.to_dict()
        elif isinstance(o, (datetime, date, time)):
            return int((o - EPOCH).total_seconds() * 1000)
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
        else:
            return super(JSONEncoder, self).default(o)

def to_json(ooo):
    return JSONEncoder(indent=2).encode(ooo)

def confirm_admin():
    if not users.is_current_user_admin():
        raise errors.NotAdmin

def confirm_dev():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        raise errors.DevModeOnly
