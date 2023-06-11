from ebotify.services.ebotifyService import EbotifyService


class BotMessageService():

    def __init__(self):
        self.__ebotifyService = EbotifyService()

    def getBotMessages(self, record):
        messages = []
        text = record.get('text')
        if text:
            messages.append(self.__ebotifyService.prepareMessage('text', text))
        data = record.get('data', {})
        if data:
            messages += self.__extractMessageFromData(data)
        return messages

    def __extractMessageFromData(self, data):
        messages = []
        image = data.get('image')
        buttons = data.get('buttons')
        quick_replies = data.get('quick_replies')
        customMessage = data.get('custom')
        attachment = data.get('attachment')
        if image:
            messages.append(
                self.__ebotifyService.prepareMessage('image', image)
            )
        if buttons:
            messages += self.__extractButtons(buttons)
        if quick_replies:
            messages += self.__extractButtons(quick_replies)
        if attachment:
            messages.append(self.__extractAttachment(attachment))
        if customMessage:
            messages+=self.__extractCustomMessage(customMessage)
        return messages

    def __extractCustomMessage(self, customMessage):
        customType = customMessage.get("type")
        attachment = customMessage.get('attachment')
        if attachment:
            return [self.__extractAttachment(attachment)]
        if customType == "calender":
            customType = customMessage.get("calender_type")
        if customMessage and customType:
            return [self.__ebotifyService.prepareMessage(customType, customMessage)]
        customMessages = []
        text = customMessage.get('text')
        image = customMessage.get('image')
        buttons = customMessage.get('buttons')
        quick_replies = customMessage.get('quick_replies')
        attachment = customMessage.get('attachment')
        if text:
            customMessages.append(self.__ebotifyService.prepareMessage('text', text))
        if image:
            customMessages.append(self.__ebotifyService.prepareMessage('image', image))
        if buttons:
            customMessages += self.__extractButtons(buttons)
        if quick_replies:
            customMessages += self.__extractButtons(quick_replies)
        if attachment:
            customMessages.append(self.__extractAttachment(attachment))
        return customMessages

    def __extractButtons(self, buttons):
        buttonMessage = []
        for button in buttons:
            buttonMessage.append(
                self.__ebotifyService.prepareMessage(
                    'button', button.get('title', '')
                )
            )
        return buttonMessage

    def __extractAttachmentUrl(self, attachment):
        return attachment.get('payload', {}).get('src', '')

    def __extractAttachment(self, attachment):
        attachmentType = attachment.get('type')
        if attachmentType in ['image', 'video', 'audio']:
            attachmentUrl = self.__extractAttachmentUrl(attachment)
            return self.__ebotifyService.prepareMessage(attachmentType, attachmentUrl)
        if attachmentType == 'document':
            url = attachment.get('document')
            return self.__ebotifyService.prepareMessage('document', url)
        if attachmentType == "template":
            return self.__extractTemplate(attachment)
        return

    def __extractTemplate(self, attachment):
        payload = attachment.get('payload', {})
        if payload.get('template_type') == "generic":
            cards = payload.get('elements', [])
            return self.__ebotifyService.prepareMessage('carousel', cards)
        return
