from pony.orm import Database, set_sql_debug, sql_debugging
import os
from urllib.parse import urlparse
from components.log import log

db = Database()


def init_db():
    database_url = os.getenv("DATABASE_URL")
    url = urlparse(database_url)

    db.bind(
        provider=url.scheme,
        host=url.hostname,
        user=url.username,
        password=url.password,
        database=url.path[1:],
        charset="utf8mb4"
    )
    db.generate_mapping(create_tables=True)

    # set_sql_debug(True)

    log.info("init db ok")
