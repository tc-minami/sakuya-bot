from slackbot.bot import respond_to
from slackbot.bot import default_reply
from slackbot.bot import listen_to

@respond_to(".*")
def respondYesIam(message):
    message.reply("お呼びでしょうか旦那様")
