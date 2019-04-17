from enum import IntEnum
from enum import auto
from slackbot.bot import respond_to
from slackbot.bot import default_reply
from slackbot.bot import listen_to
from .dbController import DBController

"""
内部クラス定義
"""

class WaitResponseID(IntEnum):
    NoWait = auto()
    DropTable = auto()

class ResponseData:

    def __init__(self):
        self.id = WaitResponseID.NoWait
        self.data = ""

    def resetData(self):
        self.id = WaitResponseID.NoWait
        self.data = ""

    def set(self, _id, _data = None):
        self.id = _id
        self.data = _data

    def isID(self, _id):
        return self.id == _id

"""
クラス変数定義
"""

dbController = DBController()
responseData = ResponseData()

"""
その他定義
"""

@respond_to(".*")
def respondYesIam(message):
    message.reply("お呼びでしょうか旦那様")

"""
DB起動／終了関連
"""

@listen_to("^[Dd][Bb][\s　]+[Ss]tart[\s　]*$")
def startDB(message):
    startDBIfNeed(message, True)

@listen_to("^[Dd][Bb][\s　]+[Ss]top[\s　]*$")
def stopDB(message):
    dbController.disconnect()
    message.reply("DB " + DBController.DB_NAME + " を終了しました。")

def startDBIfNeed(message, showMessage = False):
    if dbController.isConnected():
        return

    dbController.initializeDB(DBController.DB_NAME)
    if showMessage:
        message.reply("DB " + DBController.DB_NAME + " を初期化しました。")

"""
テーブル関連
"""

@listen_to("^[Dd][Bb][\s　]+[Tt]able[s]?[\s　][Ii]nit*$")
@listen_to("テーブル(?:初期化|作成)")
def initTables(message):
    dbController.createAllTablesIfNeed()
    message.reply("各種テーブルを初期化しました。")

@listen_to("^[Dd][Bb][\s　]+[Tt]able[s]?[\s　][Ll]ist*$")
@listen_to("テーブル(?:.*)一覧(?:.*)表示")
@listen_to("テーブル(?:.*)表示(?:.*)一覧")
def showTableNames(message):
    startDBIfNeed(message, False)

    tableNames = dbController.getTableNames();
    result = "現在登録されているテーブルはこちらです。\n"
    for index, name in enumerate(tableNames):
        result += str(index) + ". " + str(name) + "\n"
    message.reply(str(result))

@listen_to("^[Dd][Bb][\s　]+[Tt]able[s]?[\s　]+[Dd]rop[\s　]+(.+)*$")
@listen_to("テーブル(?:.*)削除[\s　]+(.+)")
def dropTable(message, tableName):
    startDBIfNeed(message, False)

    responseData.set(WaitResponseID.DropTable, tableName)
    message.reply("テーブル" + tableName + "を削除してよろしいでしょうか？")

def confirmDropTable(message):
    dbController.dropTable(responseData.data)
    message.reply("テーブル" + responseData.data + "を削除しました。")

"""
ユーザー応答待ち関連
"""

@listen_to("(?:いいえ|いや|キャンセル|[Nn][Oo]|[Cc]ancel|[Ss]top)")
def cancelWaitResponse(message):
    if not responseData.isID(WaitResponseID.NoWait):
        message.reply("処理をキャンセルしました。")
    else:
        message.reply("特に処理待ちのものはありませんよ？")
    responseData.set(WaitResponseID.NoWait)

@listen_to("(?:はい|うん|うい|[Oo][Kk]|[Oo]kay|[Yy]es|[Yy])")
def proceedWaitResponce(message):
    if responseData.isID(WaitResponseID.DropTable):
        message.reply("テーブル削除処理を遂行します。")
        confirmDropTable(message)
    elif responseData.isID(WaitResponseID.NoWait):
        message.reply("特に処理待ちのものはないようですね。")
    else:
        message.reply("想定外の処理待ちIDですわ。旦那様処理の確認をお願いします。\n現状の処理待ちID : " + str(responseData.id))
