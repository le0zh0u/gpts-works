import json
from pony.orm import db_session, set_sql_debug, sql_debugging
from components.db import db
from dtos.gptsHubGptsDTO import GptsHubGptsDTO
from dtos.gptsWorksGptsDTO import GptsWorksGptsDTO
from dtos.gptsHunterGptsDTO import GptsHunterGptsDTO

class Gpts:

    # tools
    # [1, 2, 3]
    # ["DALL•E", "Browsing", "Data Analysis"]

    # prompt_starters
    # ["starters"]

    def __init__(self, **kwargs):
        if 'gptshubDTO' in kwargs:
            self._init_from_gptshubDTO(kwargs['gptshubDTO'])
        elif 'gptsworksDTO' in kwargs:
            self._init_from_gptsworksDTO(kwargs['gptsworksDTO'])
        elif 'gptshunterDTO' in kwargs:
            self._init_from_gptshunterDTO(kwargs['gptshunterDTO'])
        # 其他初始化逻辑

    # def __init__(self, v) -> None:
    #     self.uuid = v["data"]["gizmo"]["id"]
    #     self.org_id = v["data"]["gizmo"]["organization_id"]
    #     self.name = v["data"]["gizmo"]["display"]["name"]
    #     self.description = v["data"]["gizmo"]["display"]["description"]
    #     self.avatar_url = v["data"]["gizmo"]["display"]["profile_picture_url"]
    #     self.short_url = v["data"]["gizmo"]["short_url"]
    #     self.author_id = v["data"]["gizmo"]["author"]["user_id"]
    #     self.author_name = v["data"]["gizmo"]["author"]["display_name"]
    #     self.created_at = v["created_at"]
    #     self.updated_at = v["data"]["gizmo"]["updated_at"]
    #     #self.welcome_message = v["data"]["gizmo"]["updated_at"]

    # def __init__(self, id, uuid, name, description, author_id, author_name, welcome_message, tools, prompt_starters, detail=None, avatar_url=None, short_url=None, org_id=None):
    #     self.id = id
    #     self.uuid = uuid
    #     self.org_id = org_id
    #     self.name = name
    #     self.description = description
    #     self.avatar_url = avatar_url
    #     self.short_url = short_url
    #     self.author_id = author_id
    #     self.author_name = author_name
    #     self.welcome_message = welcome_message
    #     self.tools = tools
    #     self.prompt_starters = prompt_starters
        # self.detail = detail

    def _init_from_gptshubDTO(self, gptshubDTO:GptsHubGptsDTO):
        #self.tags = tags
        self.uuid = gptshubDTO.id
        self.org_id = ""
        self.name = gptshubDTO.name
        self.description = gptshubDTO.description
        self.avatar_url = ("https://files.oaiusercontent.com/" + gptshubDTO.logo) if gptshubDTO.logo else ""
        self.short_url = gptshubDTO.id
        self.author_id = ""
        self.author_name = gptshubDTO.author
        self.welcome_message = gptshubDTO.welcome_message
        self.tools = gptshubDTO.tools
        self.prompt_starters = gptshubDTO.prompt_starters
        # self.created_at = gptshubDTO.updated_at
        # self.updated_at = gptshubDTO.updated_at

    def _init_from_gptsworksDTO(self, gptsworksDTO: GptsWorksGptsDTO):
        self.uuid = gptsworksDTO.uuid
        self.org_id = gptsworksDTO.org_id
        self.name = gptsworksDTO.name
        self.description = gptsworksDTO.description
        self.avatar_url = gptsworksDTO.avatar_url
        self.short_url = gptsworksDTO.short_url
        self.author_id = gptsworksDTO.author_id
        self.author_name = gptsworksDTO.author_name
        # self.created_at = gptsworksDTO.created_at
        # self.updated_at = gptsworksDTO.updated_at
        self.detail = gptsworksDTO.detail
        self.welcome_message = None
        self.tools = None
        self.prompt_starters = None

    def _init_from_gptshunterDTO(self, gptshunterDTO: GptsHunterGptsDTO):

        gpt_unique_id = gptshunterDTO.gpt_unique_id
        parts = gpt_unique_id.split('-')

        self.uuid = '-'.join(parts[:2])        
        self.org_id = None
        self.name = gptshunterDTO.name
        self.description = gptshunterDTO.desc
        image = gptshunterDTO.image
        if image is None or image == "null":
            self.avatar_url = None
        else:
            self.avatar_url = image

        self.short_url = gpt_unique_id
        self.author_id = None
        if gptshunterDTO.author is None or gptshunterDTO.author == "--":
            self.author_name = ""
        else:
            self.author_name = gptshunterDTO.author

        self.detail = None

        self.welcome_message = gptshunterDTO.welcome_message

        self.prompt_starters = gptshunterDTO.starters

        tools = []
        for tool in gptshunterDTO.tools:
            if tool == "python" or tool == "plugins_prototype":
                tools.append(3)
            elif tool == "browser":
                tools.append(2)
            elif tool == "dalle":
                tools.append(1)
            else:
                print("GptsHunterGptsDTO -> Gpts, tools has unknown value ", tool)
        
        self.tools = list(set(tools))



# def get_gpts_from_file(file_ame: str):
#     with open(file_name, 'r', encoding='utf-8') as file:
#         data = json.load(file)
#         gpts = []
#         for v in data:
#             gpt = Gpts(v)
#             print("gpts: ", gpt.name, gpt.uuid)
#             gpts.append(gpt)
            
#         return gpts


@db_session
def get_gpts_from_db(last_id: int, limit: int):
    if limit <= 0:
        limit = 100

    rows = db.select(
        "SELECT * FROM gpts WHERE id > $last_id AND index_updated_at = 0 ORDER BY id asc LIMIT $limit"
    )
    gpts = []
    for row in rows:
        gpts.append(row)

    return gpts


@db_session
def get_gpts_by_uuids(uuids: [str]):
    rows = db.select(
        "SELECT * FROM gpts WHERE uuid = ANY($uuids) ORDER BY id asc"
    )
    gpts = []
    for row in rows:
        gpts.append(row)

    return gpts


@db_session
def update_gpts_index_time(ids: [int], index_time: int):
    db.execute("UPDATE gpts SET index_updated_at=$index_time WHERE id = ANY($ids)")

    return

@db_session
def save_gpt(gpt: Gpts):
    # with sql_debugging(show_values=True): 
    # 检查是否已存在该UUID的记录
    existing = db.select("SELECT id FROM gpts WHERE uuid = $gpt.uuid")
    tools = ','.join(map(str, gpt.tools)) if gpt.tools else ''
    prompt_starters = ','.join(map(str, gpt.prompt_starters)) if gpt.prompt_starters else ''
    if existing:
        # 更新现有记录
        db.execute(
            "UPDATE gpts SET name=$gpt.name, description=$gpt.description, "
            "author_id=$gpt.author_id, author_name=$gpt.author_name, welcome_message=$gpt.welcome_message, "
            "tools=$tools, prompt_starters=$prompt_starters, "
            "avatar_url=$gpt.avatar_url, short_url=$gpt.short_url, org_id=$gpt.org_id  "
            "WHERE uuid=$gpt.uuid"
        )

        return 2
    else:
        # 插入新记录
        db.execute(
            "INSERT INTO gpts (uuid, org_id, name, description, avatar_url, short_url, author_id, author_name, welcome_message, tools, prompt_starters ) "
            "VALUES ($gpt.uuid, $gpt.org_id, $gpt.name, $gpt.description, $gpt.avatar_url, $gpt.short_url, $gpt.author_id, $gpt.author_name, $gpt.welcome_message, $tools, $prompt_starters )"
        )

        return 1

