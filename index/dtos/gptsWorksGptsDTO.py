class GptsWorksGptsDTO:
    def __init__(self, v) -> None:
        self.uuid = v["uuid"]
        self.org_id = v["org_id"]
        self.name = v["name"]
        self.description = v["description"]
        self.avatar_url = v["avatar_url"]
        self.short_url = v["short_url"]
        self.author_id = v["author_id"]
        self.author_name = v["author_name"]
        self.created_at = v["created_at"]
        self.updated_at = v["updated_at"]
        self.detail = v.get("detail", None)