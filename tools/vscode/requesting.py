import requests
import simplejson
import json

def send_request():
    url = 'http://localhost:3000/'
    with open("tests/newfile.json", "r") as file:
        data = json.load(file)
    # data_json = simplejson.dumps(data)
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print('Response:', response.json())
    else:
        print('Failed to get a valid response. Status code:', response.status_code)

if __name__ == "__main__":
    send_request()
