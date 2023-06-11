import time
import sys
sys.path.append(".")
from ebotify.database.sqliteDb import Database
from ebotify.logger import logger
from ebotify.settings.setting import CRON_TIME_IN_SECONDS
from ebotify.services.eventService import EventService


class EbotifyProcessor:

    def __init__(self) -> None:
      self.__cronTime = CRON_TIME_IN_SECONDS
      self.__eventService = EventService()

    def startProcessor(self):
        while True:
            try:
                self.__eventService.processEvents()
            except Exception as e:
                logger.error(e)
            finally:
                time.sleep(self.__cronTime)

if __name__ == "__main__":
    Database().createDbTables()
    ebotifyProcessor = EbotifyProcessor()
    ebotifyProcessor.startProcessor()
