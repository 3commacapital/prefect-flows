import requests
import base64


class CFBenchmark:
    base_url = "https://www.cfbenchmarks.com/api/v1"
    def __init__(self, api_key):
        self.api_key = api_key

    def headers(self):
        credentials = base64.b64encode(self.api_key.encode('ascii'))
        return { "Authorization": f"Basic {credentials.decode('ascii')}" }

    def get(self, url):
        return requests.get(f"{self.base_url}{url}", headers=self.headers())

    def values(self, id):
        url = f"/values?id={id}"
        return self.get(url).json().get('payload')