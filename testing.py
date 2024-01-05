import json
import requests

with open('newmem.json', 'r',encoding='utf-8') as file:
    json_data = json.load(file)

ids = [item['user']['id'] for item in json_data['data']]

# Simpan IDs ke dalam file sebagai array
with open('newmemid.json', 'w') as file:
    json.dump(ids, file)

