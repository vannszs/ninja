import json
import requests

# Proxy details
proxy = {
    'http': 'http://172.16.0.1:44355',
}


# Lakukan request ke API dengan menggunakan proxy
response = requests.get("https://ninja.garden/api/points/leaderboard", proxies=proxy)

# Pastikan request berhasil dan responsenya valid
if response.status_code == 200:
    data = response.json()["data"]

    # Ambil nilai id dari setiap objek dalam data
    ids = [entry["user"]["id"] for entry in data]

print(ids)
