import os
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str


def load():
    return Config(api_key=os.environ['API_KEY'])


config = load()


@dataclass
class ConfigApi:
    http_key: str


def load_api():
    return ConfigApi(http_key=os.environ['HTTP_KEY'])


config_api = load_api()
