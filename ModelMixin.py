"""
Common Functionality for all model
"""

#
# NDB classes should add this mixin so that they can be properly serilized with an id representing
# the key
# example
# class Tag(ModelMixin, ndb.Model):
# 
class ModelMixin(object):
    # to_dict ends up being called when serializing models to json
    # this puts the key in there as "id"
    def to_dict(self):
        result = super(ModelMixin, self).to_dict()
        result['id'] = self.key.id()
        return result
