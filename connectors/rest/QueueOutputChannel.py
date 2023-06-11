from asyncio import Queue
from typing import NoReturn, Text, Dict, Any, Optional
from rasa.core.channels.channel import (
    CollectingOutputChannel,
)
from constants.connector import QUEUE
from constants.logger import NOT_IMPLEMENTED_ERROR


class QueueOutputChannel(CollectingOutputChannel):
    @classmethod
    def name(cls) -> Text:
        return QUEUE

    def __init__(self, message_queue: Optional[Queue] = None) -> None:
        super().__init__()
        self.messages = Queue() if not message_queue else message_queue

    def latest_output(self) -> NoReturn:
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)

    async def _persist_message(self, message: Dict[Text, Any]) -> None:
        await self.messages.put(message)