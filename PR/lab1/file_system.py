import json

def write_json(name, data):
    with open(name, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def read_json(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
    return data