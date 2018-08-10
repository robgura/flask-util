"""
Contains errors for the project
"""

class ParentRequired(Exception):
    pass

class InvalidParent(Exception):
    pass

class NotAdmin(Exception):
    pass

class DevModeOnly(Exception):
    pass

class CouldNotFindId(Exception):
    def __init__(self, kind, idd):
        super(CouldNotFindId, self).__init__()
        self.kind = kind
        self.id = idd

class MissingKey(Exception):
    def __init__(self, key):
        super(MissingKey, self).__init__()
        self.key = key

class Duplicate(Exception):
    def __init__(self, tt):
        super(Duplicate, self).__init__()
        self.type = tt
