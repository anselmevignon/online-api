#!/usr/bin/env python
""" implement simple REST request to online.net api """
import logging
import os
import json
import slumber
from fire import Fire
from jsonpath_rw import parse
from requests import session


logging.basicConfig(level=os.getenv("ONLINE_DEBUG_LVL", "INFO"))
ONLINE_BASE_URL = 'https://api.online.net/api/v1'

TOKEN_FILE = os.getenv(
    "ONLINE_TOKEN_FILE",
    "/etc/online.secret")


def __read_conf():
    "read the conf file, extracting the access token"
    with open(TOKEN_FILE, 'r') as read:
        toktok = json.load(read)
    return toktok["access_token"]

AUTH_TOKEN = __read_conf()


def get_session():
    "build a session with fixed authentication"
    curr_session = session()
    curr_session.headers["Authorization"] = \
        "Bearer %s" % AUTH_TOKEN
    return curr_session


def _api():
    "internal function, build the api"
    curr_session = get_session()
    return slumber.API(ONLINE_BASE_URL, session=curr_session)

api = _api()  # pylint: disable=invalid-name


class CliAPI(object):
    """Get data from online from bash
    The avalailable data and formats are described in
    https://console.online.net/en/api/
    """

    def get(self, rest_path):  # pylint: disable=no-self-use
        "get data in json form"
        curr_session = get_session()
        return curr_session.get(ONLINE_BASE_URL+"/"+rest_path).json

    def get_parsed(self, rest_path, jsonpath):  # pylint: disable=no-self-use
        """get data in json form.
        The result is parsed using jsonpath expression
        jsonpath is basically Xpath for json, see:
        https://pypi.python.org/pypi/jsonpath-rw
        for requirements
        """
        curr_session = get_session()
        output = curr_session.get(ONLINE_BASE_URL+"/"+rest_path).json()
        return [m.value for m in parse(jsonpath).find(output)]

if __name__ == "__main__":
    Fire(CliAPI)
