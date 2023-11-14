
import requests
import json
from models.gpts import save_gpt, Gpts
from dtos.gptsHubGptsDTO import GptsHubGptsDTO

def get_gptshub_from_file():
    print("start to read data from file")
    with open('data/gptshub.json', 'r', encoding='utf-8') as file:
        print("file opened")
        data = json.load(file)
        gpts = []
        for v in data:
            gpt = GptsHubGptsDTO(v)
            print("gpts: ", gpt.name, gpt.id)
            gpts.append(gpt)

        print("finished read data")
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

def import_from_gptshub():
    
    # get data
    gptsList = fetch_gptshub_json()
    if gptsList is None or len(gptsList) == 0:
        return 
    print("get gptsList: count:", len(gptsList))

    # save gpts

    success_count = 0
    failed_count = 0
    for gpts in gptsList:

        try: 
            save_gpt(gpt=Gpts(gptshubDTO=gpts))
            success_count += 1
        except Exception as e:
            print("save gpt failed", e, gpts.name, gpts.id)
            failed_count += 1

    print("save result, success: {}, failed: {}", success_count, failed_count)



