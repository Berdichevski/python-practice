import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests

url = "https://plenty-readers-poke.loca.lt/suggest"
headers = {
    'User-Agent': 'MyUserAgent/1.0',
    'Authorization': 'Bearer some_token'
}

response = requests.get(url, headers = headers, params = {'w': ''})

if response.status_code == 200:
    print(response.text)
else:
    print(response.status_code)