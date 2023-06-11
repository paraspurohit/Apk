import json
import logging
import requests

from config.dotEnv import API_KEY, TENANT_ID
from ebotify.constants.ebotifyConstant import CHANNELS_ID
from ebotify.database.sqliteDb import Tickets
from ebotify.helpers.timestampHelper import TimestampHelper
from ebotify.repositories.ebotifyRepository import EbotifyRepository

logger = logging.getLogger(__name__)


class TicketService():

    def __init__(self) -> None:
        self._timestampHelper = TimestampHelper()
        self.__ebotifyRepository = EbotifyRepository()
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def addTicket(self, senderId, ticketId):
        ticketDetails = [Tickets(
            senderId=senderId,
            ticketId=ticketId
        )]
        return self.__ebotifyRepository.addTicket(ticketDetails)

    def getAllTickets(self):
        return self.__ebotifyRepository.getAllTickets()(Tickets)

    def getTicketBySenderId(self, senderId):
        filter = Tickets.senderId == senderId
        return self.__ebotifyRepository.getTicketsByFilter(filter)

    def deleteTicketBySenderId(self, senderId):
        condition = (Tickets.senderId == senderId)
        return self.__ebotifyRepository.deleteTicket(condition)

    def getEbotifyTicket(self, messages, sender, senderId, timestamp, info):
        ticketDetails = self.getTicketBySenderId(senderId)
        if ticketDetails:
            logger.info("Ticket Found")
            ticketNo = ticketDetails[0].ticketId
        else:
            ticketNo = self.createTicketOnEbotify(
                messages, sender, senderId, timestamp, info)
        return ticketNo

    def createTicketOnEbotify(self, messages, sender, senderId, timestamp, info):
        logger.info("Ticket not found")
        payload = {
            "tenantId": TENANT_ID,
            "apiKey": API_KEY,
            "messages": messages,
            "sender": sender,
            "senderId": senderId,
            "channel": CHANNELS_ID.get("rest"),
            "ebotifyCustomerId": senderId,
            "channelUniqueId": senderId,
            "timestamp": timestamp,
            "info": info
        }
        payload = json.dumps(payload)
        response = requests.post(
            self.__liveagentUrl, data=payload, headers=self.headers)
        logger.info(response)
        if response.status_code != 200:
            return None
        resJson = response.json()
        logger.info(f"Response from Ebotify Create Ticket: {resJson}")
        ticketId = resJson.get('body').get('ticketNo')
        self.addTicket(senderId, ticketId)
        return ticketId

    def defaultInfo(self, senderId, name=None):
        if not name:
            name = "Web User"
        info = [{
            "key": "name",
            "value": name
        },
            {
            "key": "uniqueId",
            "value": senderId
        },
            {
            "key": "biriId",
            "value": senderId
        }]
        return info

    def regenerateTicket(self, senderId, name=None):
        self.deleteTicketBySenderId(senderId)
        messages = []
        sender = 2
        timestamp = self._timestampHelper.getNanoSecondTimestamp()
        info = self.defaultInfo(senderId, name)
        return self.createTicketOnEbotify(messages, sender, senderId, timestamp, info)
