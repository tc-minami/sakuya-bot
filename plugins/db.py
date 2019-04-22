import sqlite3
import re
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

    def executeAndCommit(self, sql, data = None):
        if not self.isConnected(True):
            return False
        self.__cursor.execute(sql) if data is None else self.__cursor.execute(sql, data)
        self.__conn.commit()
        return self.__cursor

    def execute(self, sql, data = None):
        if not self.isConnected(True):
            return False
        self.__cursor.execute(sql) if data is None else self.__cursor.execute(sql, data)
        return self.__cursor

    def count(self, sql):
        if not self.isConnected(True):
            return False
        self.__cursor.execute(sql)
        result = self.__cursor.fetchall()
        count = 0 if result is None else len(result)
        print("Row Count = " + str(count))
        return str(count)

    def commit(self):
        if not self.isConnected(True):
            return False
        self.__conn.commit()

    def fetchall(self):
        if not self.isConnected(True):
            return False
        self.__cursor.fetchall()

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
            result.append(str(re.sub("^(\(\')|(\'\,\))$", "", str(name))))

        return result

    """
    その他Util関連
    """
    def createDateTimeStr(self, time = datetime.now()):
        return time.strftime("%Y/%m/%d_%H:%M:%S")
