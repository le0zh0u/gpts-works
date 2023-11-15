from models.gpts import save_gpt, Gpts
from services.data_source.gpts_hub import fetch_gptshub_json
from services.data_source.gpts_works import fetch_gptsworks_data_random
from services.data_source.gpts_hunter import fetch_gptshunter_from_file
import sys
import time
from components.log import log

def import_from_gptshunter():

    gptsList = fetch_gptshunter_from_file()
    if gptsList is None or len(gptsList) == 0:
        return {"count":0}
    count = len(gptsList)
    log.info("get gptsList: count - %d", count)

    # save gpts
    insert_count = 0
    update_count = 0
    failed_count = 0
    for gpts in gptsList:
        # print("gpts: ", gpts.name, gpts.uuid)
        try: 
            result = save_gpt(gpt=Gpts(gptshunterDTO=gpts))
            if result == 1:
                insert_count += 1
            elif result == 2:
                update_count += 1
        except Exception as e:
            log.error("save gpt failed, e - %s, name - %s, id - %s", e, gpts.name, gpts.id)
            failed_count += 1
   
    log.info("save result, insert - %d, update - %d, failed - %d", insert_count, update_count, failed_count)
    return {"count": count, "insert_count": insert_count, "update_count": update_count, "failed_count": failed_count}


def import_from_gptsworks():
    gptsList = fetch_gptsworks_data_random(last_id=0, limit=1000)
    if gptsList is None or len(gptsList) == 0:
        return {"count": 0}
    
    count = len(gptsList)
    log.info("get gptsList: count - %d", count)

    # save gpts
    insert_count = 0
    update_count = 0
    failed_count = 0
    for gpts in gptsList:
        # print("gpts: ", gpts.name, gpts.uuid)
        try: 
            result = save_gpt(gpt=Gpts(gptsworksDTO=gpts))
            if result == 1:
                insert_count += 1
            elif result == 2:
                update_count += 1
        except Exception as e:
            log.error("save gpt failed, e - %s, name - %s, id - %s", e, gpts.name, gpts.id)
            failed_count += 1
   
    log.info("save result, insert - %d, update - %d, failed - %d", insert_count, update_count, failed_count)
    return {"count": count, "insert_count": insert_count, "update_count": update_count, "failed_count": failed_count}


def import_from_gptshub():
    
    # get data
    gptsList = fetch_gptshub_json()
    if gptsList is None or len(gptsList) == 0:
        return {"count": 0}
    
    count = len(gptsList)
    log.info("get gptsList: count - %d", count)

    # save gpts

    insert_count = 0
    update_count = 0
    failed_count = 0
    for index, gpts in enumerate(gptsList):
        try: 
            result = save_gpt(gpt=Gpts(gptshubDTO=gpts))
            if result == 1:
                insert_count += 1
            elif result == 2:
                update_count += 1

        except Exception as e:
            log.error("save gpt failed, e - %s, name - %s, id - %s", e, gpts.name, gpts.id)
            failed_count += 1
        # i = int(index * 100 / count)
        # print("Download progress: {}%: ".format(i), "▋" * (i // 2), end="")
        # sys.stdout.flush()

    log.info("save result, insert - %d, update - %d, failed - %d", insert_count, update_count, failed_count)
    return {"count": count, "insert_count": insert_count, "update_count": update_count, "failed_count": failed_count}



