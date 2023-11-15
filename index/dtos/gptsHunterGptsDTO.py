class GptsHunterGptsDTO:
     def __init__(self, v) -> None:

        self.currentUrl = v["currentUrl"]
        self.name = v["name"]
        self.update_at_text = v["updateAtText"]
        self.image = v["image"]
        self.update_at = v["updateAt"]
        self.desc = v["desc"]
        self.author = v["author"]
        self.linked_domain = v["linkedDomain"]
        self.welcome_message = v["welcomeMessage"]
        self.gpt_link = v["gptlink"]
        self.gpt_unique_id = v["gptUniqueId"]
        self.starters = v["starters"]
        self.tools = v["tools"]
        # "tools": [
        #     "python",
        #     "browser",
        #     "dalle"
        # ]
        