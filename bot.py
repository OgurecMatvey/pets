import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

#users_greeted = set()  #

def write_msg(user_id, message, attachment=None):
    params = {
        "user_id": user_id,
        "message": message,
        "random_id": random.randint(1, 2147483647)
    }
    if attachment:
        params["attachment"] = attachment
    vk.method("messages.send", params)

token = "vk1.a.zkj5dqnFtA5-K-IyLcXE2C7_t65vCodwTn0AzF5C8ogMY1W_pW3jV_Rn1a_OJ1ZagB1zxVpBAYBsVJeHPhY6DgvstQd57eOuvtxR3LQbBF95pF2XjpZu8KQSRfQRhT66Hm_F43r1c7ytvKX-swn48R7806nal1zRVvexSRZsU-kvAaRO7Rnr2jKKgGl0nGbVP1z36_6a52kOAh9w2LxznA"

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
#        if event.user_id not in users_greeted:
#            write_msg(event.user_id, "Привет! Я бот, который может отправлять обратно ваши изображения. Отправьте мне картинку!")
#            users_greeted.add(event.user_id)
#            continue

        message = vk.method("messages.getById", {"message_ids": [event.message_id]})
        attachments = message['items'][0].get('attachments', [])
        
        if attachments and attachments[0]['type'] == 'photo':
            photo = attachments[0]['photo']
            attachment = f"photo{photo['owner_id']}_{photo['id']}"
            if 'access_key' in photo:
                attachment += f"_{photo['access_key']}"
            write_msg(event.user_id, "", attachment)
        else:
            write_msg(event.user_id, "Пожалуйста, отправьте изображение!")
