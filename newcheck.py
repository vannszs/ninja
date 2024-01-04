import json
import requests

# Mendapatkan data JSON dari API
response = requests.get("https://ninja.garden/api/points/leaderboard")

# Pastikan request berhasil dan responsenya valid
if response.status_code == 200:
    data = response.json()["data"]

# Baca data JSON dari file leaderboard.json
with open('leaderboard.json', 'r',encoding='utf-8') as file:
    json_data = json.load(file)["data"]

# Ambil semua ID dari data yang ada di leaderboard.json
ids = [item["user"]["id"] for item in json_data]

newmem = []

# Membandingkan setiap data dari API dengan data yang ada di leaderboard.json
for item in data:
    if item["user"]["id"] not in ids:
        newmem.append(item)

# Menyimpan data newmem ke dalam file newmem.json
with open('newmem.json', 'w') as file:
    json.dump(newmem, file)
