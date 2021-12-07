import json


def encode_json_for_mqtt(key, runtime):
    return json.dumps({"key": key, "runtime": runtime})


def decode_json_from_mqtt(x):
    return json.loads(x)
