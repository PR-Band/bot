import os
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str


def load():
    return Config(api_key=os.environ['API_KEY'])


config = load()
