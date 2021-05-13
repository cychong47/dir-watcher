#!/bin/env python3
import sys
import time
import os

telegram_token = os.environ['TELEGRAM_API_TOKEN']
telegram_chatid = os.environ['TELEGRAM_CHAT_ID']

class MyTelegram():
    fake = False

    def __init__(self, token=telegram_token, chat_id=telegram_chatid, fake=False):
        self.fake = fake

        if self.fake == False:
            import telegram
            try:
                self.bot = telegram.Bot(token=token)
            except:
                print("fail to get token(%s). just exit" %token)
                sys.exit(0)

            self.chat_id = chat_id

    def send_msg(self, msg):
        if self.fake == True:
            return

        try:
            self.bot.sendMessage(self.chat_id, text=msg)
        except:
            print("fail to send msg(chat_id %s)" %self.chat_id)

    def get_update(self):
        if self.fake == True:
            return None

        return self.bot.getUpdates()

if __name__ == "__main__":
    tg = MyTelegram(telegram_token, telegram_chatid)

#    message = sys.argv[1] if len(sys.argv) > 1 else 'howdy'
    message = "howdy"
    tg.send_msg(message)
