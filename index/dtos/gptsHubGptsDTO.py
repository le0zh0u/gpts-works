
#tool 1,2,3
# g = ["DALL•E", "Browsing", "Data Analysis"]

class GptsHubGptsDTO:
    def __init__(self, id, name, author, description, updated_at, tags, prompt_starters, welcome_message, tools, logo):
        self.id = id
        self.name = name
        self.author = author
        self.description = description
        self.updated_at = updated_at
        self.tags = tags
        self.prompt_starters = prompt_starters
        self.welcome_message = welcome_message
        self.tools = tools
        self.logo = logo

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            author=data.get('author'),
            description=data.get('description'),
            updated_at=data.get('updated_at'),
            tags=data.get('tags'),
            prompt_starters=data.get('prompt_starters'),
            welcome_message=data.get('welcome_message'),
            tools=data.get('tools'),
            logo=data.get('logo')
        )
    
    def __init__(self, v) -> None:
        self.id = v["id"]
        self.name = v["name"]
        self.author = v["author"]
        self.description = v["description"]
        self.updated_at = v["updated_at"]
        self.tags = v["tags"]
        self.prompt_starters = v["prompt_starters"]
        self.welcome_message = v["welcome_message"]
        self.tools = v["tools"]
        self.logo = v.get("logo", None)
        #self.welcome_message = v["data"]["gizmo"]["updated_at"]
