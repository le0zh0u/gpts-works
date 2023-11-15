# data source: gpts.works
import requests
import json

from dtos.gptsWorksGptsDTO import GptsWorksGptsDTO

def fetch_gptsworks_data_random(last_id: int = 0, limit: int = 500): 
    url = 'https://gpts.works/api/gptsall'
    headers = {
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'accept': '*/*',
        'origin': 'https://gpts.works'
    }

    payload = {
        'last_id': last_id,
        'limit': limit
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 检查响应
    response.raise_for_status()

    data = response.json().get("data")
    if data is None:
        return None
    rows = data.get("rows")
    if rows is None or len(rows) == 0:
        return None
    gpts = []
    for v in rows:
        gpt = GptsWorksGptsDTO(v)
        # print("gpts: ", gpt.name, gpt.id)
        gpts.append(gpt)

    # print("finished read data")
    return gpts


#     curl 'https://gpts.works/api/gptsall' \
#   -H 'authority: gpts.works' \
#   -H 'accept: */*' \
#   -H 'accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7' \
#   -H 'content-type: application/json' \
#   -H 'dnt: 1' \
#   -H 'origin: https://gpts.works' \
#   -H 'referer: https://gpts.works/' \
#   -H 'sec-ch-ua: "Chromium";v="119", "Not?A_Brand";v="24"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36' \
#   --data-raw '{"last_id":0,"limit":100}' \
#   --compressed
