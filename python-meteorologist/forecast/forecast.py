import simplejson as json
import requests

# TODO: Documentation


class Forecast(object):
    def __init__(self, user_agent: str = '') -> None:
        if len(user_agent) < 1:
            raise TypeError('User Agent is required.')  # maybe change error or make new one
        else:
            self.user_agent = user_agent
