import os
from os.path import join, dirname
from dotenv import load_dotenv

# .envを読み込む
env_path = join(dirname(__file__), '.env')
load_dotenv(env_path)

# .envからbotアカウントのトークンを取得
API_TOKEN = os.environ.get("API_TOKEN")

# このBotが行う処理が見つからなかった時に返すメッセージ
DEFAULT_REPLY = "ご指示を理解できませんでした。もう一度お願いいたします。"

# プラグインスクリプトを置いてあるサブディレクトリ名
PLUGINS = ['plugins']
