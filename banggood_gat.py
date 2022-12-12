import json
import requests

from requests.structures import CaseInsensitiveDict

class GAT:
    def get_access_token():
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        url = "https://api.banggood.com/getAccessToken?app_id=app_id&app_secret=app_secret"
        response = requests.get(url, headers=headers)
        response = json.loads(response.text)
        # print("GAT response")
        # print(response)
        access_token_file =  open('access_token', 'w', encoding='utf-8')
        access_token_file.write(response["access_token"])

        return response["access_token"]

#GAT.get_access_token()
