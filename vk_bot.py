import os
import random
from create_intent import detect_intent_texts
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import google.cloud.dialogflow_v2 as dialogflow

LANGUAGE_CODE = 'ru'


def handle_message(event, vk_api, project_id):
    vk_session_id = f"vk_{event.user_id}"
    dialogflow_response = detect_intent_texts(
        project_id=project_id,
        session_id=vk_session_id,
        user_message=event.text,
        language_code='ru'
        )

    is_response_fallback = dialogflow_response.query_result.intent.is_fallback
    if not is_response_fallback:
        text = dialogflow_response.query_result.fulfillment_text
        vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()

    API_KEY_VK_BOT = os.environ['API_KEY_VK_BOT']
    project_id = os.environ['PROJECT_ID']
    GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    vk_session = vk.VkApi(token=API_KEY_VK_BOT)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("VK бот запущен и слушает сообщения...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api)


if __name__ == "__main__":
    main()

