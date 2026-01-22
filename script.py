from google.cloud import dialogflow_v2 as dialogflow

credential_path = 'C:/Users/user/service-account.json'
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

project_id = "speech001-t9mm"
session_id = '645860380'
language_code = 'ru'  

# Создаем клиента
session_client = dialogflow.SessionsClient()
session = session_client.session_path(project_id, session_id)

# Входящее сообщение
text_input = dialogflow.TextInput(text='Ваш вопрос', language_code=language_code)
query_input = dialogflow.QueryInput(text=text_input)

# Отправляем запрос
response = session_client.detect_intent(request={'session': session, 'query_input': query_input})

# Получаем ответ
print('Ответ:', response.query_result.fulfillment_text)