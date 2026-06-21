# import requests
from curl_cffi import requests
import json 

response = requests.get(
  "https://tls.peet.ws/api/all",
  impersonate="chrome120"
)

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#     "Accept": "application/json"
# }
# response = requests.get("https://tls.peet.ws/api/all", headers=headers)
# response = requests.get("https://ja3er.com")




print(json.dumps(response.json(), indent=4))