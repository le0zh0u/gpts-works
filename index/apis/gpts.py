from fastapi import APIRouter, Header, BackgroundTasks
from pydantic import BaseModel
from services.index import build_index_for_gpts_list
from services.search import search_gpts
from utils.resp import resp_err, resp_ok, resp_data
from utils.time import get_current_timestamp
from models.gpts import get_gpts_from_db, update_gpts_index_time
from services.dataProvider import import_from_gptshub, import_from_gptsworks, import_from_gptshunter
import os

gpts_router = APIRouter()

@gpts_router.get("/gpts/import/gptshunter")
async def import_gpts_from_gptshunter(background_tasks: BackgroundTasks, authorization: str = Header(None)):
    # try:
        background_tasks.add_task(import_from_gptshunter)
        return resp_ok("ok")
        # result = import_from_gptshunter()
        # return resp_ok("ok")
    # except Exception as e:
    #     print("import gpts from gptshub failed:", e)
    #     return resp_err(f"{e}")

@gpts_router.get("/gpts/import/gtpsworks")
async def import_gpts_from_gptsworks(background_tasks: BackgroundTasks, authorization: str = Header(None)):
    # try:
    #     result = import_from_gptsworks()
    #     return resp_data(result)
    # except Exception as e:
    #     print("import gpts from gptshub failed:", e)
    #     return resp_err(f"{e}")
    background_tasks.add_task(import_from_gptsworks)
    return resp_ok("ok")


@gpts_router.get("/gpts/import/gptshub")
async def import_gpts_from_gptshub(background_tasks: BackgroundTasks, authorization: str = Header(None)):
    # indexApiKey = os.getenv("INDEX_API_KEY")
    # authApiKey = ""
    # if authorization:
    #     authApiKey = authorization.replace("Bearer ", "")
    # if authApiKey != indexApiKey:
    #     return resp_err("Access Denied")
    background_tasks.add_task(import_from_gptshub)
    return resp_ok("ok")
    # try:
    #     result = import_from_gptshub()
    #     return resp_data(result)
    # except Exception as e:
    #     print("import gpts from gptshub failed:", e)
    #     return resp_err(f"{e}")

@gpts_router.post("/gpts/index")
async def build_gpts_index(authorization: str = Header(None)):
    indexApiKey = os.getenv("INDEX_API_KEY")
    authApiKey = ""
    if authorization:
        authApiKey = authorization.replace("Bearer ", "")
    if authApiKey != indexApiKey:
        return resp_err("Access Denied")

    try:
        last_id = 0
        limit = 300

        while True:
            # get a batch gpts
            gpts = get_gpts_from_db(last_id=last_id, limit=limit)
            if gpts is None or len(gpts) == 0:
                return resp_ok("ok")

            # build index for batch articles
            res = build_index_for_gpts_list(gptsList=gpts)
            if res is None:
                return resp_err("build gpts index failed")

            # update index_time
            index_time = get_current_timestamp()
            index_ids = [a.id for a in gpts]
            print("update index time", index_time, index_ids)
            update_gpts_index_time(ids=index_ids, index_time=index_time)

            last_id = gpts[len(gpts) - 1].id
    except Exception as e:
        print("build gpts index failed:", e)
        return resp_err(f"{e}")



class SearchReq(BaseModel):
    question: str


@gpts_router.post("/gpts/search")
async def search_gpts_with_question(req: SearchReq, authorization: str = Header(None)):
    indexApiKey = os.getenv("INDEX_API_KEY")
    authApiKey = ""
    if authorization:
        authApiKey = authorization.replace("Bearer ", "")
    if authApiKey != indexApiKey:
        return resp_err("Access Denied")

    if req.question == "":
        return resp_err("invalid params")

    try:
        gpts = search_gpts(question=req.question)

        return resp_data(gpts)
    except Exception as e:
        return resp_err(f"{e}")
