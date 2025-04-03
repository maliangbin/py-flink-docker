import json
from src.model.stat_model import StatModel
from pyflink.common.typeinfo import Types
from pyflink.common.types import Row


class CleanService:
    def __init__(self):
        pass

    def clean(self, data: str):
        try:
            json_obj = json.loads(data)

            # 构建清洗数据
            stat_model = StatModel()
            clean_data = stat_model.fillable(json_obj)
        except Exception as e:
            # logging.exception(e)
            print(f"Invalid JSON data: {data}")
            return None

        if not clean_data or not isinstance(clean_data, dict):
            return None

        return clean_data

    def appId(self, app_id):
        return int(app_id)

    def dict_to_row(self, data: dict):
        return Row(**data)

    @staticmethod
    def get_type_info():
        stat_model = StatModel()
        field_names, field_types = stat_model.get_type_info()
        return Types.ROW_NAMED(field_names, field_types)
