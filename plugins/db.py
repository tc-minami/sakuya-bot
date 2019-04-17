import sqlite3
from datetime import datetime

class DB:

    def __init__(self):
        self.currentDBName = ""
        self.__conn = None
        self.__cursor = None

    """
    DBアクセス関連
    """

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

    """
    SQL関連
    """

    def executeAndCommit(self, sql):
        if not self.isConnected(True):
            return False
        self.__cursor.execute(sql)
        self.__conn.commit()

    def execute(self, sql):
        if not self.isConnected(True):
            return False
        self.__cursor.execute(sql)

    def commit(self):
        if not self.isConnected(True):
            return False
        self.__conn.commit()

    """
    Table関連
    """

    # Returns array of table names.
    def getTableNames(self):
        result = []
        if not self.isConnected(True):
            return result

        self.execute("select name from sqlite_master where type=\"table\"")

        for name in self.__cursor.fetchall():
            result.append(name)

        return result
