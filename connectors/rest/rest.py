import asyncio
import inspect
import json
import logging
from asyncio import Queue, CancelledError
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable
import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from connectors.rest.QueueOutputChannel import QueueOutputChannel
from constants.connector import INPUT_CHANNEL, MESSAGE, PAYLOAD, POSTBACK, R_MESSAGE_ID, RATING_RESPONSE, RESPONSE_TYPE, REST, SENDER
from constants.logger import BODY_FOR_INVALID_REQUEST, CANCELLED_ERROR, EXCEPTION_USER_MESSAGE
from constants.messageType import RATING, TEXT, TYPE

logger = logging.getLogger(__name__)


class RestInput(InputChannel):

    @classmethod
    def name(cls) -> Text:
        return REST

    @staticmethod
    async def on_message_wrapper(
        on_new_message: Callable[[UserMessage], Awaitable[Any]],
        text: Text,
        queue: Queue,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> None:
        collector = QueueOutputChannel(queue)
        message = UserMessage(text,
                              collector,
                              sender_id,
                              input_channel=input_channel,
                              metadata=metadata)
        await on_new_message(message)
        await queue.put("DONE")

    async def _extract_sender(self, req: Request) -> Optional[Text]:
        return req.json.get(SENDER, None)

    def _extract_message(self, req: Request) -> Optional[Text]:
        reqJson = req.json
        if self.is_response_type_rating(reqJson):
            return RATING_RESPONSE
        messageType = reqJson.get(MESSAGE,{}).get(TYPE)
        if messageType == POSTBACK:
            return reqJson.get(MESSAGE,{}).get(messageType).get(PAYLOAD)
        if messageType == TEXT:
            return reqJson.get(MESSAGE,{}).get(messageType)
        return req.json.get(MESSAGE, None)

    def is_response_type_rating(self, response: Request):
        response_type = response.get(RESPONSE_TYPE)
        if response_type == RATING:
            return True
        return False

    def _extract_input_channel(self, req: Request) -> Text:
        return req.json.get(INPUT_CHANNEL) or self.name()

    def get_metadata(self, req: Request):
        resJson = req.json
        if self.is_response_type_rating(resJson):
            ignoreHistory = self.ignore_history(req.json)
            user_feedback = resJson.get(RATING)
            rMessageId = resJson.get(R_MESSAGE_ID)
            return {"user_feedback": user_feedback,
                    R_MESSAGE_ID: rMessageId,
                    "ignoreHistory":ignoreHistory
                }
        messageType = resJson.get(MESSAGE, {}).get(TYPE)
        if messageType == POSTBACK:
            return{
                "msgType": messageType,
                messageType: resJson.get(MESSAGE, {}).get(messageType)
            }
        return resJson.get("metadata", None)

    def ignore_history(self, reqJson):
        metadata = reqJson.get("metadata")
        if metadata and metadata.get("ignoreHistory"):
            return True
        return False

    def stream_response(
        self,
        on_new_message: Callable[[UserMessage], Awaitable[None]],
        text: Text,
        sender_id: Text,
        input_channel: Text,
        metadata: Optional[Dict[Text, Any]],
    ) -> Callable[[Any], Awaitable[None]]:
        async def stream(resp: Any) -> None:
            q = Queue()
            task = asyncio.ensure_future(
                self.on_message_wrapper(on_new_message, text, q, sender_id,
                                        input_channel, metadata))
            while True:
                result = await q.get()
                if result == "DONE":
                    break
                else:
                    await resp.write(json.dumps(result) + "\n")
            await task
        return stream

    def blueprint(
            self, on_new_message: Callable[[UserMessage],
                                           Awaitable[None]]) -> Blueprint:
        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            logger.info(request.json)
            sender_id = await self._extract_sender(request)
            text = self._extract_message(request)
            if text is None or sender_id is None:
                return response.json(status=400,body=BODY_FOR_INVALID_REQUEST)
            should_use_stream = rasa.utils.endpoints.bool_arg(request,
                                                              "stream",
                                                              default=False)
            input_channel = self._extract_input_channel(request)
            metadata = self.get_metadata(request)
            logger.info(metadata)
            if should_use_stream:
                return response.stream(
                    self.stream_response(on_new_message, text, sender_id,
                                         input_channel, metadata),
                    content_type="text/event-stream",
                )
            else:
                collector = CollectingOutputChannel()
                try:
                    await on_new_message(
                        UserMessage(
                            text,
                            collector,
                            sender_id,
                            input_channel=input_channel,
                            metadata=metadata,
                        ))
                except CancelledError:
                    logger.error(CANCELLED_ERROR.format(text))
                except Exception:
                    logger.exception(EXCEPTION_USER_MESSAGE.format(text))
                return response.json(collector.messages)
        return custom_webhook