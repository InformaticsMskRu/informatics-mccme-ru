import json
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator, Text


class JsonType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value, separators=(',', ':'))

    def process_result_value(self, value, dialect):
        if not value:
            return None
        try:
            loaded = json.loads(value)
        except json.JSONDecodeError:
            loaded = None
        return loaded


class MutableDict(Mutable, dict):
    @classmethod
    def coerce(cls, key, value):
        "Convert plain dictionaries to MutableDict."

        if not isinstance(value, MutableDict):
            if isinstance(value, dict):
                return MutableDict(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __setitem__(self, key, value):
        "Detect dictionary set events and emit change events."

        dict.__setitem__(self, key, value)
        self.changed()

    def __delitem__(self, key):
        "Detect dictionary del events and emit change events."

        dict.__delitem__(self, key)
        self.changed()
