import json
from config.dotEnv import API_KEY, IS_LIVE_AGENT, TENANT_ID
from ebotify.constants.ebotifyConstant import BOT_CHANNEL, CHANNELS_ID, SENDER_TYPE
from ebotify.database.sqliteDb import Events
from ebotify.logger import logger
from ebotify.repositories.ebotifyRepository import EbotifyRepository
from ebotify.services.botMessageService import BotMessageService
from ebotify.services.ebotifyService import EbotifyService, MessagePayload
from ebotify.services.messageInfoService import MessageInfoService
from ebotify.services.ticketService import TicketService
from ebotify.services.userMessageService import UserMessageService


class EventService():

    def __init__(self):
        self.__ebotifyRepository = EbotifyRepository()
        self.__botMessage = BotMessageService()
        self.__userMessage = UserMessageService()
        self.__ticketService = TicketService()
        self.__messageInfoService = MessageInfoService()
        self.__ebotifyService = EbotifyService()

    def processEvents(self):
        filters = self.__eventFilters()
        events = self.__ebotifyRepository.getEventsByFilter(*filters)
        self.processMessages(events)
        return

    def processMessages(self, events):
        for event in events:
            try:
                eventData = json.loads(event.data)
                payload = self.preparePayload(eventData)
                res = self.__ebotifyService.sendMessage(payload)
                logger.info(res)
            except Exception as ex:
                logger.error(ex)
            finally:
                self.__ebotifyRepository.deleteEvent((Events.id <= event.id))
                return

    def preparePayload(self, record):
        sessionId = self.getSessionId(record)
        senderType = SENDER_TYPE.get(record.get("event"))
        messages = self.getMessages(record)
        if not messages:
            raise Exception("No messages found")
        channel = self.getChannelId()
        timestamp = self.getTimestamp(record)
        info = self.getInfo(record, senderType, channel)
        ticketNo = None
        ignoreTicket = False

        if IS_LIVE_AGENT:
            ticketNo = self.__ticketService.getEbotifyTicket(
                messages,
                senderType,
                sessionId,
                timestamp,
                info
            )
        else:
            ignoreTicket = True
        return MessagePayload(
            sessionId,
            TENANT_ID,
            API_KEY,
            messages,
            senderType,
            channel,
            timestamp,
            info,
            sessionId,
            sessionId,
            ignoreTicket=ignoreTicket,
            ticketNo=ticketNo
        ).dict()

    def getSessionId(self, record):
        return record.get("sender_id")

    def getTimestamp(self, record):
        return record.get("timestamp") * 1000000000

    def getChannelId(self):
        return CHANNELS_ID.get(BOT_CHANNEL)

    def getMessages(self, record):
        if record.get("event") == 'user':
            return self.__userMessage.getUserMessage(record)
        elif record.get("event") == 'bot':
            return self.__botMessage.getBotMessages(record)
        return

    def getInfo(self, record, sender, channel):
        return self.__messageInfoService.getMessageInfo(sender, channel, record)

    def __eventFilters(self):
        containsProductName = Events.data.contains('"event": "user"')
        containsProductBrand = Events.data.contains('"event": "bot"')
        filters = []
        filter = containsProductName | containsProductBrand
        filters.append(filter)
        return tuple(filters)
