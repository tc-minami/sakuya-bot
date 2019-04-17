import sqlite3
from datetime import datetime

class DB:

    def __init__(self):
        self.currentDBName = ""
        self.__conn = None
        self.__cursor = None

    def connect(self, dbName, disconnectIfConnected = True):
        if self.isConnected(False):
            print("Is connected to " + self.currentDBName + "already.")
            if disconnectIfConnected:
                self.disconnect()

        self.__conn = sqlite3.connect(dbName, check_same_thread = False)
        self.__cursor = self.__conn.cursor()
        self.currentDBName = dbName
        print("Connected to " + self.currentDBName + ".")

    def disconnect(self):
        if self.__conn is not None:
            self.__conn.close()

        print("Disconnected from " + self.currentDBName + ".")
        self.__conn = None
        self.__cursor = None
        self.currentDBName = ""

    def isConnected(self, showErrorLogIfNotConnected = False):
        result = self.__conn is not None and self.__cursor is not None
        if not result and showErrorLogIfNotConnected:
            print("[ALERT] DB is not connected.")
        return result
