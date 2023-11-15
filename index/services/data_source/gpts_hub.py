import requests
import json
from dtos.gptsHubGptsDTO import GptsHubGptsDTO

# data source: gpts_hub

def get_gptshub_from_file():
    # print("start to read data from file")
    with open('data/gptshub.json', 'r', encoding='utf-8') as file:
        # print("file opened")
        data = json.load(file)
        gpts = []
        for v in data:
            gpt = GptsHubGptsDTO(v)
            # print("gpts: ", gpt.name, gpt.id)
            gpts.append(gpt)

        # print("finished read data")
        return gpts

def fetch_gptshub_json():
    url = "https://raw.githubusercontent.com/lencx/GPTHub/main/gpthub.json"
    response = requests.get(url)
    response.raise_for_status()  # 确保响应状态是200

    gpts = []
    for v in response.json().get("gpts"):
        gpt = GptsHubGptsDTO(v)
        # print("gpts: ", gpt.name, gpt.id)
        gpts.append(gpt)
        
    return gpts