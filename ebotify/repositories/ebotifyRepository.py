from ebotify.database.sqliteDb import Database, Tickets, Events


class EbotifyRepository():

    def __init__(self):
        self.__Db = Database()

    def getAllEvents(self):
        return self.__Db.query(Events).all()

    def getEventsByFilter(self, *filter):
        return self.__Db.query(Events).filter(*filter).all()

    def deleteEvent(self, condition):
        return self.__Db.deleteRecord(Events, condition)

    def addTicket(self, ticketRecord):
        return self.__Db.addRecord(ticketRecord)

    def getAllTickets(self):
        return self.__Db.query(Tickets).all()

    def getTicketsByFilter(self, *filter):
        return self.__Db.query(Tickets).filter(*filter).all()

    def deleteTicket(self, condition):
        return self.__Db.deleteRecord(Tickets, condition)
