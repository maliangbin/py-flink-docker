from src.model.base_model import BaseModel


class StatModel(BaseModel):
    fillable_fields = {
        "device_id": "string",
        "open_id": "string",
        "union_id": "string",
        "user_id": "int",
        "phone": "string",
        "request_id": "string",
        "session_id": "string",
        "appid": "int",
        "ua": "string",
        "os": "string",
        "os_version": "string",
        "brand": "string",
        "device_model": "string",
        "carrier": "int",
        "network_type": "int",
        "install_source": "string",
        "resolution": "string",
        "sdk_version": "string",
        "coordinates": "string",
        "coordinates_address": "string",
        "province": "string",
        "city": "string",
        "district": "string",
        "street": "string",
        "event_ts": "long",
        "report_ts": "long",
        "event": "string",
        "action": "string",
        "path": "string",
        "referer": "string",
        "element_id": "string",
        "is_new_device": "string",
        "ipv4": "string",
        "ipv6": "string",
    }

    def __init__(self):
        pass
