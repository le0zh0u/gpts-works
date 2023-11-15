# data source: gpts hunter
import json
from dtos.gptsHunterGptsDTO import GptsHunterGptsDTO

def fetch_gptshunter_from_file():
    # print("start to read data from file")
    with open('data/gptshunter.json', 'r', encoding='utf-8') as file:
        # print("file opened")
        data = json.load(file)
        gpts = []
        for v in data:
            gpt = GptsHunterGptsDTO(v)
            # print("gpts: ", gpt.name, gpt.id)
            gpts.append(gpt)

        # print("finished read data")
        return gpts
