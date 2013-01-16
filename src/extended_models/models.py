from django.db import models

import json

class SerializableModel(models.Model):
    def normalize(self):
        return {}

    def to_json(self):
        return json.dumps(self.normalize())

    class Meta:
        abstract = True


class SerializableList(list):
    def to_json(self):
        return json.dumps([o.to_json() for o in self])
