import json
import requests

username = 'BPM'
password = 'SageVIP@0824'
base_url = 'https://try.oacey.com:9443'
api_key = 'c1a8f1dd-9155-4918-bc26-ec030488a742'
endpoint = 'api/apibase/GenericGet/EMP_JOB_GRD'

session = requests.Session()
payload = {
    "scope": f"apiKey={api_key}",
    "username": username,
    "password": password,
    "grant_type": "password",
    }

response = session.post(
                f"{base_url}/token",
                data=payload
            )


access_token = json.loads(response.content)["access_token"]

session.headers = {"Authorization": f"Bearer {access_token}"}

url = f"{base_url}/{endpoint}"
response = session.post(url)

print(json.loads(response.content))




