import json
import requests
from config.dotEnv import EBOTIFY_URL
from config.dotEnv import IS_LIVE_AGENT
from ebotify.logger import logger


class EbotifyService():

    def __init__(self):
        self.headers = {
            "content-type": "application/json"
        }

    def prepareMessage(self, messageType, message):
        return {
            "type": messageType,
            "message": message
        }

    def sendMessage(self, payload):
        data = json.dumps(payload)
        logger.info(payload)
        return requests.post(EBOTIFY_URL, headers=self.headers, data=data)


class MessagePayload():

    def __init__(self, sessionId: str, tenantId: str, apiKey: str, messages: list, sender: int, channel: int, timestamp: float, info: list, ebotifyCustomerId: str, channelUniqueId: str, ignoreTicket: bool = False, ticketNo: str = None) -> None:
        self.sessionId = sessionId
        self.tenantId = tenantId
        self.apiKey = apiKey
        self.messages = messages
        self.sender = sender
        self.channel = channel
        self.timestamp = timestamp
        self.info = info
        self.ebotifyCustomerId = ebotifyCustomerId
        self.channelUniqueId = channelUniqueId
        if not IS_LIVE_AGENT or ignoreTicket:
            self.ignoreTicket = ignoreTicket
        elif ticketNo:
            self.ticketNo = ticketNo
        else:
            raise Exception("Ticket No is required")

    def dict(self):
        return self.__dict__
