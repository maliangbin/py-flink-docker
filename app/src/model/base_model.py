from pyflink.common.typeinfo import Types


class BaseModel:
    _ROW_TYPE_MAPPING = {
        "string": Types.STRING,
        "int": Types.INT,
        "long": Types.LONG,
        "double": Types.DOUBLE,
        "float": Types.FLOAT,
        "boolean": Types.BOOLEAN,
        "byte": Types.BYTE,
        "bigint": Types.BIG_INT,
        "char": Types.CHAR,
    }

    _TYPE_MAPPING = {
        "string": lambda x: str(x),
        "int": lambda x: int(x),
        "long": lambda x: int(x),
        "double": lambda x: int(x),
        "boolean": lambda x: bool(x),
        "float": lambda x: float(x),
        "bigint": lambda x: int(x),
        "char": lambda x: str(x),
    }

    def __init__(self):
        pass

    def fillable(self, data: dict):
        fillable_fields = self.fillable_fields

        clean_data = {}

        for field, type in fillable_fields.items():
            value = data.get(field)
            clean_data[field] = self.type_handler(type, value)

        return clean_data

    def type_handler(self, type, value):
        handler = self._TYPE_MAPPING.get(type, lambda value: value)
        return handler(value)

    def type_handler_type(self, type):
        handler = self._ROW_TYPE_MAPPING[type]
        return handler()

    def get_type_info(self):
        fillable_fields = self.fillable_fields
        type_info = []
        for field, type in fillable_fields.items():
            type_info.append(self.type_handler_type(type))

        field_names = list(fillable_fields.keys())
        field_types = type_info
        return field_names, field_types
