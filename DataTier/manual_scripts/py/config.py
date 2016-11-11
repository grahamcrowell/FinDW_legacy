import json

json_path='dataFolderConfig.json'
f = open(json_path).read()
config=json.loads(f)

print(config['statement']['loaded'])
