from ebotify.settings.setting import IS_KB_ACTIVE
from ebotify.services.ebotifyService import EbotifyService


class UserMessageService():

    def __init__(self):
        self.__ebotifyService = EbotifyService()

    def getUserMessage(self, record):
        metadata = record.get('metadata')
        messageType = self.__getMessageType(metadata)
        if messageType == 'text':
            return [self.__extractTextMessage(record)]
        if messageType == 'button':
            return [self.__extractButtonMessage(metadata)]
        if messageType == 'image':
            return [self.__extractImageMessage(metadata)]
        if messageType == 'video':
            return [self.__extractVideoMessage(metadata)]
        if messageType == 'document':
            return [self.__extractDocMessage(metadata)]
        if messageType == 'audio':
            return [self.__extractAudioMessage(metadata)]
        return

    def __extractTextMessage(self, record):
        text = record.get('text', '')
        if IS_KB_ACTIVE:
            text= self.__extractKbText(text)
        return self.__ebotifyService.prepareMessage('text', text)

    def __extractButtonMessage(self, metadata):
        return self.__ebotifyService.prepareMessage('button', metadata.get('title', ''))

    def __extractImageMessage(self, metadata):
        return self.__ebotifyService.prepareMessage('image', metadata.get('image', ''))

    def __extractVideoMessage(self, metadata):
        return self.__ebotifyService.prepareMessage('video', metadata.get('video', ''))

    def __extractAudioMessage(self, metadata):
        return self.__ebotifyService.prepareMessage('audio', metadata.get('audio', ''))

    def __extractDocMessage(self, metadata):
        return self.__ebotifyService.prepareMessage('document', metadata.get('document', ''))

    def __getMessageType(self, metadata):
        return metadata.get('messageType', 'text')

    def __extractKbText(self, text):
        if text.startswith("/e_kb_"):
            splitedtext = text.split("_")
            text = ' '.join(splitedtext[3:])
        return text
