import os
import random
from create_intent import create_intent
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv
import google.cloud.dialogflow_v2 as dialogflow

load_dotenv()

API_KEY_VK_BOT = os.environ['API_KEY_VK_BOT']
project_id = os.environ['PROJECT_ID']
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
LANGUAGE_CODE = 'ru'

session_client = dialogflow.SessionsClient()

def detect_intent_texts(project_id, session_id, text, language_code):
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})
    return response.query_result.fulfillment_text

def handle_message(event, vk_api):
    user_id = event.user_id
    user_message = event.text
    session_id = str(user_id)
    try:
        reply = detect_intent_texts(project_id, session_id, user_message, LANGUAGE_CODE)
        vk_api.messages.send(
            user_id=user_id,
            message=reply,
            random_id=random.randint(1, 100000)
        )
    except Exception as e:
        vk_api.messages.send(
            user_id=user_id,
            message="Произошла ошибка при обработке сообщения.",
            random_id=random.randint(1, 100000)
        )
        print(f"Error: {e}")

def main():
    load_dotenv()
    vk_session = vk.VkApi(token=API_KEY_VK_BOT)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    print("VK бот запущен и слушает сообщения...")

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, vk_api)

if __name__ == "__main__":
    main()

