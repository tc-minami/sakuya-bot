from enum import IntEnum
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from .db import DB

class Status(IntEnum):
    Hide = 0
    Show = 1

class DBController:

    #DB SETTINGS
    DB_NAME = "mainDB.db"

    # TABLE
    __TABLE_DEF = "table_default"
    __TABLE_FAMILY_TASKS = "table_family_tasks"
    __TABLE_FAMILY_MISTAKES = "table_family_mistakes"
    __TABLE_FAMILY_TODO = "table_family_todo"
    __TABLE_FAMILY_CATEGORY = "table_family_category"

    def __init__(self):
        self.db = DB()

    def initializeDB(self, dbName):
        self.db.connect(dbName)

    def disconnect(self):
        self.db.disconnect()

    def isConnected(self):
        return self.db.isConnected()

    """
    Category Table用Data操作関連
    """

    # sort_order : 0が先頭に表示される
    def addData2FamilyCategory(self, category, sort_order, status):

        count = self.db.count("select * from " + DBController.__TABLE_FAMILY_CATEGORY + " where category is '" + category + "'")
        print("Category " + category + " の一致件数 = " + str(count))

        if int(count) > 0:
            return

        count = self.db.count("select * from " + DBController.__TABLE_FAMILY_CATEGORY + " where sort_order is '" + sort_order + "'")
        print("SortOrder " + sort_order + " の一致件数 = " + str(count))

        if int(count) > 0:
            return

        sql = "insert into " + DBController.__TABLE_FAMILY_CATEGORY + " "
        sql += """
        (category, sort_order, status, create_at, last_update)
        values (?, ?, ?, ?, ?)
        """
        timeStr = self.db.createDateTimeStr()
        data = (category, sort_order, status, timeStr, timeStr)
        self.db.executeAndCommit(sql, data)

    def getAllDataFromFamilyCategory(self):
        result = []
        for row in self.db.execute("select * from " + DBController.__TABLE_FAMILY_CATEGORY + " order by sort_order asc"):
            result.append(row)
        return result

    def countFamilyCategoryWithSortOrder(self, sortOrder):
        self.db.execute("select count(sort_order = " + sortOrder + ") from " + __TABLE_FAMILY_CATEGORY)

    """
    汎用Table用Data操作関連
    """

    def getCurrentDateTime(self):
        return self.db.createDateTimeStr()

    """
    Table操作関連
    """

    def getTableNames(self):
        return self.db.getTableNames()

    def dropTable(self, tableName, commit = True):
        sql = "drop table if exists " + tableName
        self.db.executeAndCommit(sql) if commit else self.db.execute(sql)

    """
    Table作成関連
    """
    def createAllTablesIfNeed(self):
        self.createTableDefaultIfNeed(False)
        self.createTableFamilyCategory(False)
        self.createTableFamilyTasksIfNeed(False)
        self.db.commit()

    def createTableDefaultIfNeed(self, commit = True):
        sql = "create table if not exists " + DBController.__TABLE_DEF + " "
        sql += """
        (id integer primary key,
        key text not null,
        value text,
        create_at text not null,
        last_update text not null
        )
        """
        self.db.executeAndCommit(sql) if commit else self.db.execute(sql)
        print("Table " + DBController.__TABLE_DEF + " の登録を完了。")

    def createTableFamilyCategory(self, commit = True):
        sql = "create table if not exists " + DBController.__TABLE_FAMILY_CATEGORY + " "
        sql += """
        (id integer primary key,
        category text not null unique,
        sort_order integer not null unique,
        status integer not null,
        create_at text not null,
        last_update text not null
        )
        """
        self.db.executeAndCommit(sql) if commit else self.db.execute(sql)
        print("Table " + DBController.__TABLE_FAMILY_CATEGORY + " の登録を完了。")

    def createTableFamilyTasksIfNeed(self, commit = True):
        sql = "create table if not exists " + DBController.__TABLE_FAMILY_TASKS + " "
        sql += """
        (id integer primary key,
        category text not null,
        content text not null,
        description text,
        status integer not null,
        create_at text not null,
        last_update text not null
        )
        """
        self.db.executeAndCommit(sql) if commit else self.db.execute(sql)
        print("Table " + DBController.__TABLE_FAMILY_TASKS + " の登録を完了。")
