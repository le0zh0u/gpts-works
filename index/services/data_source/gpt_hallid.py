# data source: https://gpts.hallid.ai/

import requests
import json


def fetch_hallid_json():
    url = ""
    response = requests.get(url)
    response.raise_for_status()

    