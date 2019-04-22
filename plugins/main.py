from enum import IntEnum
from enum import auto
from slackbot.bot import respond_to
from slackbot.bot import default_reply
from slackbot.bot import listen_to
from .dbController import DBController
from .dbController import Status

"""
内部クラス定義
"""

class WaitResponseID(IntEnum):
    NoWait = auto()
    DropTable = auto()
    AddData = auto()
    AddDataCategory = auto()

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
    message.reply("お呼びでしょうか旦那様。")

# @listen_to("(.+)")
# def listen2All(message, content):
#     if responseData.isID(WaitResponseID.AddDataCategory):
#         value = re.search(r"^[\s　]*(\w+)[\s　]+(\d+)[\s　]*$")
#         message.reply

@listen_to("時間")
def showCurrentTime(message):
    message.reply("今の時間は" + dbController.getCurrentDateTime() + "です。")

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
データ関連
"""
# @listen_to("(?:データ)(?:.*)(?:追加|登録)")
# def addData(message):
#     startDBIfNeed(message, False)
#     response = "データを追加します。追加先を選んでください。\n"
#     response += __getTableNames(True)
#     responseData.set(WaitResponseID.AddData)
#     message.reply(response)

@listen_to("(?:(?:追加|登録)(?:.*)カテゴリ)|(?:カテゴリ(?:.*)(?:追加|登録))[\s　]+(.+)[\s　](.+)+")
@listen_to("(?:(?:[Aa]dd|[Rr]egister|[Ss]et])(?:.*)[Cc]ategory)|(?:[Cc]ategory(?:.*)(?:[Aa]dd|[Rr]egister|[Ss]et]))")
def addData(message, category, sortId):
    startDBIfNeed(message, False)

    responseData.set(WaitResponseID.AddDataCategory)
    message.reply("カテゴリ : " + category + " ソート番号 : " + sortId + " を追加します。")

    dbController.addData2FamilyCategory(category, sortId, Status.Show)

    result = dbController.getAllDataFromFamilyCategory()

    for row in result:
        message.reply(str(row))



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
    result = "現在登録されているテーブルはこちらです。\n"
    result += __getTableNames(True)
    message.reply(str(result))

def __getTableNames(showIndex = True):
    tableNames = dbController.getTableNames();
    result = ""
    if showIndex:
        for index, name in enumerate(tableNames):
            result += str(index) + ". " + str(name) + "\n"
    else:
        for name in tableNames:
            result += str(name) + "\n"
    return result

def __getTableName(index):
    tableNames = dbController.getTableNames();
    return tableNames[int(index)]

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

@listen_to("^(?:いいえ|いや|キャンセル|[Nn][Oo]|[Cc]ancel|[Ss]top)$")
def cancelWaitResponse(message):
    if not responseData.isID(WaitResponseID.NoWait):
        message.reply("処理をキャンセルしました。")
    else:
        message.reply("特に処理待ちのものはありませんよ？")
    responseData.set(WaitResponseID.NoWait)

@listen_to("^(?:はい|うん|うい|[Oo][Kk]|[Oo]kay|[Yy]es|[Yy])$")
def proceedWaitResponse(message):
    if responseData.isID(WaitResponseID.DropTable):
        message.reply("テーブル削除処理を遂行します。")
        confirmDropTable(message)
    elif responseData.isID(WaitResponseID.NoWait):
        message.reply("特に処理待ちのものはないようですね。")
    else:
        message.reply("想定外の処理待ちIDですわ。旦那様処理の確認をお願いします。\n現状の処理待ちID : " + str(responseData.id))

# @listen_to("^(\d+)$")
# def proceedWaitResponseNumeric(message, index):
#     if responseData.isID(WaitResponseID.NoWait):
#         return
#     elif responseData.isID(WaitResponseID.AddData):
#         responseData.set(WaitResponseID.AddDataCategory)
#         message.reply("テーブル" + str(__getTableName(index)) + "を選択しました。\nカテゴリ名とソート番号を指定してください。")
