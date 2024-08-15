import requests 
import json

uri = "https://data.paris2024.org/api/explore/v2.1/catalog/datasets"

try: 
    data = requests.get(uri)
    data.raise_for_status()
    js_data = json.loads(data.text)
    with open("olympia2024.json", "w") as f:
        json.dump(js_data, f, indent=4)
except Exception as e:
    print(e)

