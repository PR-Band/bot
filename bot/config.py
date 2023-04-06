import os
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str
    http_key: str


def load():
    return Config(api_key=os.environ['API_KEY'], http_key=os.environ['HTTP_KEY'])


config = load()
