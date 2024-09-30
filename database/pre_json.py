import json

data = None

with open("config.json", 'r') as f:
    data = json.load(f)

print(type(data))
print(data)