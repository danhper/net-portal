from django.db import models

import json

class SerializableModel(models.Model):
    def normalize(self):
        raise NotImplementedError("Override normalize method to use SerializableModel")

    def to_json(self):
        return json.dumps(self.normalize())

    class Meta:
        abstract = True


class SerializableList(list):
    def normalize(self):
        return [v.normalize() for v in self]

    def to_json(self):
        return json.dumps(self.normalize())
