import requests
import json

# Create your tests here.
ABSOLUTE_URL = "http://127.0.0.1:8000/employee/api/"


def post_data():
    json_data = {
        'e_no': 111,
        'e_name': 'Kishore',
        'e_sal': 5000,
        'e_addr': 'Hyderbad'
    }
    resp = requests.post(url=ABSOLUTE_URL, data=json.dumps(json_data))
    print(f"Response : {resp.status_code}")
    print(f"Response : {resp.text}")


def get_data(id):
    resp = requests.get(url=ABSOLUTE_URL, data=json.dumps({'e_no': id}))
    print(f"Response : {resp.status_code}")
    print(f"Response : {resp.text}")


get_data(None)
