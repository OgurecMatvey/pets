import os
from telethon.sync import TelegramClient
from telethon import functions
import time

api_id = "YOUR_ID"
api_hash = "YOUR_HASH"

with TelegramClient('session_name', api_id, api_hash) as client:
    client.connect()
    for i in range(100):
        try:
            print("Обновляем био...")
            result = client(functions.account.UpdateProfileRequest(
                about=f'{i}'
            ))
            print(f"Теперь ваше био: {i}")
            time.sleep(120) 
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(120)  
