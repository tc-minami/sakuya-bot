from slackbot.bot import respond_to
from slackbot.bot import listen_to
from .db import DB

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
