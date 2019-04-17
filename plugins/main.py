from slackbot.bot import respond_to
from slackbot.bot import default_reply
from slackbot.bot import listen_to
from .dbController import DBController

dbController = DBController()


@respond_to(".*")
def respondYesIam(message):
    message.reply("お呼びでしょうか旦那様")

@listen_to("^[Dd][Bb][\s　]+[Ss]tart[\s　]*$")
def startDB(message):
    startDBIfNeed(message, True)

@listen_to("^[Dd][Bb][\s　]+[Ss]top[\s　]*$")
def stopDB(message):
    dbController.disconnect()
    message.reply("DB " + DBController.DB_NAME + " を終了しました。")

@listen_to("^[Dd][Bb][\s　]+[Tt]able[s]?[\s　][Ii]nit*$")
@listen_to("テーブル初期化")
def initTables(message):
    dbController.createAllTablesIfNeed()
    message.reply("各種テーブルを初期化しました。")

@listen_to("^[Dd][Bb][\s　]+[Tt]able[s]?[\s　][Ll]ist*$")
@listen_to("テーブル一覧表示")
def showTableNames(message):
    startDBIfNeed(message, False)

    tableNames = dbController.getTableNames();
    result = "現在登録されているテーブルはこちらです。\n"
    for index, name in enumerate(tableNames):
        result += str(index) + ". " + str(name) + "\n"
    message.reply(str(result))

@listen_to("^[Dd][Bb][\s　]+[Tt]able[s]?[\s　]+[Dd]rop[\s　]+(.+)*$")
@listen_to("テーブル削除[\s　]+(.+)")
def dropTable(message, tableName):
    dbController.dropTable(tableName)
    message.reply("テーブル" + tableName + "を削除しました。")

def startDBIfNeed(message, showMessage = False):
    if dbController.isConnected():
        return

    dbController.initializeDB(DBController.DB_NAME)
    if showMessage:
        message.reply("DB " + DBController.DB_NAME + " を初期化しました。")
