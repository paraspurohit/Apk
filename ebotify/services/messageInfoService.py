from ebotify.settings.setting import IS_KB_ACTIVE
from ebotify.constants.feedbackIntents import IGNORE_FEEDBACK_INTENTS
from ebotify.constants.intentConstants import INTENTS


class MessageInfoService():

    def getMessageInfo(self, senderType, channel, record):
        info = []
        info.append(self.__getName(channel, record))
        if senderType == 2:
            info+=self.__getIntentInfo(record)
        return info

    def __getName(self, channel, record):
        name = self.__extractNameFromRecord(record)
        if name:
            return name
        name = self.__getNameFromChannel(channel)
        return self.__createInfo('name', name)

    def __createInfo(self, key, value):
        return {'key': key, 'value': value}

    def __extractNameFromRecord(self, record):
        return record.get('metadata', {}).get('name')

    def __getNameFromChannel(self, channel):
        if channel == 0:
            return 'WhatsApp User'
        if channel == 1:
            return 'Telegram User'
        if channel == 2:
            return 'Web User'
        if channel == 5:
            return 'SMS User'
        if channel == 6:
            return 'Facebook User'
        return 'ebotify User'

    def __getIntentInfo(self, record):
        intentInfo = []
        intent = record.get('parse_data', {}).get('intent').get('name')
        if intent in INTENTS:
            intentData = INTENTS.get(intent)
            intentName = intentData.get("friendlyIntent")
            ignoreIntent = intentData.get("ignoreIntent")
            intentInfo.append(self.__createInfo('intent', intentName))
            intentInfo.append(self.__createInfo('ignoreIntent', ignoreIntent))
        if IS_KB_ACTIVE:
            intentInfo += self._addKbInfo(intent, record)
            intentInfo.append(self.__createInfo('kb', 'true'))
        return intentInfo

    def _addKbInfo(self, intent, record):
        kbInfo = []
        messageId = record.get('message_id')
        intentConfidence = intent.get('confidence')
        if messageId:
            kbInfo.append(self.__createInfo('rMessageId', messageId))
        if intentConfidence:
            kbInfo.append(
                self.__createInfo(
                    'intentConfidence', intentConfidence
                )
            )
        if intent.get('name', '') in IGNORE_FEEDBACK_INTENTS:
            ignoreFeedback = 'true'
        else:
            ignoreFeedback = 'false'
        kbInfo.append(self.__createInfo('ignoreFeedback', ignoreFeedback))
        return kbInfo
