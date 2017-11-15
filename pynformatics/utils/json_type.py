import json
from sqlalchemy.types import TypeDecorator, Text


class JsonType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return None
        try:
            loaded = json.loads(value)
        except json.JSONDecodeError:
            loaded = None
        return loaded


