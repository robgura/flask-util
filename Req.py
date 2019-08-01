"""
utility functions to share among models
"""
from werkzeug.exceptions import BadRequestKeyError
import errors

class Req(object):
    def __init__(self, req):
        self.req = req
        self.json = None

    def is_get(self):
        return self.req.method == 'GET'

    def is_post(self):
        return self.req.method == 'POST'

    def is_put(self):
        return self.req.method == 'PUT'

    def get_form(self):
        return self.req.form

    def get_json(self):
        # cache self.json
        if self.json != None:
            return self.json

        self.json = self.req.get_json(force=True)
        return self.json

    def get_value(self, tag):
        j_data = self.get_json()
        if tag not in j_data:
            raise errors.MissingKey(tag)

        return j_data[tag]

    def get_value_as_int(self, tag):
        return int(self.get_value(tag))

    def has_arg(self, tag):
        return tag in self.req.args

    def get_arg(self, tag):
        try:
            return self.req.args[tag]
        except BadRequestKeyError:
            raise errors.MissingKey(tag)

    def get_arg_as_int(self, tag):
        return int(self.get_arg(tag))

    def get_arg_int_list(self, tag):
        if tag not in self.req.args:
            raise errors.MissingKey(tag)

        int_list = [int(x) for x in self.req.args[tag].split(',')]
        return int_list

class TestReq(object):
    """
    class used to mock Req class in tests
    """
    def __init__(self, obj):
        self.obj = obj

    def get_value(self, tag):
        if tag not in self.obj:
            raise errors.MissingKey(tag)

        return self.obj[tag]

    def get_value_as_int(self, tag):
        return int(self.get_value(tag))

    def get_json(self):
        return self.obj
