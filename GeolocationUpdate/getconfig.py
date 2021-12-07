import json


def get_config():
    r"""
    Read information out of config file.

    :return: dict

    """
    f = open("c:/Users/dilGoe/Desktop/UniSem5/" +
             "GeolocationUpdate/config.json")
    config = json.load(f)
    return config
