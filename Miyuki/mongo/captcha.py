# Copyright (C) 2022 venujast
# Copyright (C) 2021 @themiyukixbot

# This file is part of @themiyukixbot (Telegram Bot)

from pymongo import MongoClient
from Miyuki import MONGO_URL

class captchas():
    def __init__(self):
        self.db = MongoClient(MONGO_URL)["captcha"]
        self.chats = self.db["Chats"]
        
    def chat_in_db(self, chat_id):
        chat = self.chats.find_one({"chat_id":chat_id})
        return chat
        
    def add_chat(self, chat_id, captcha):
        if self.chat_in_db(chat_id):
            return 404
        self.chats.insert_one({"chat_id":chat_id, "captcha": captcha})
        return 200
    
    def delete_chat(self,chat_id):
        self.chats.delete_many({"chat_id": chat_id})
        return True