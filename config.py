import os
from dataclasses import dataclass

@dataclass
class Config:
    api_key: str



def load():
    return Config(api_key=os.environ['API_KEY'])


# @dataclass
# class Config_db:
#     db_url: str


# def load_db():
#     return Config_db(db_url=os.environ['DB_URL'])



config = load()
# config_db = load_db
