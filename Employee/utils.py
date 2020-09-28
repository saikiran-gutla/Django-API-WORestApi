import json


def is_valid_json(data):
    try:
        p_data = json.loads(data)
        print(f"UTILS DATA :{p_data}")
        valid_json = True
    except KeyError:
        valid_json = False
    except TypeError:
        valid_json = False
    return valid_json
