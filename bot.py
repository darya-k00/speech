from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow_v2 as dialogflow
import os
from create_intent import create_intent
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']

credential_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
project_id = os.environ['PROJECT_ID']
language_code = 'ru'

session_client = dialogflow.SessionsClient()

def detect_intent_texts(project_id, session_id, texts, language_code):
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=texts, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={'session': session, 'query_input': query_input})
    return response.query_result.fulfillment_text

def start(update, context):
    update.message.reply_text("Привет! Я бот, созданный при поддержке DialogFlow)")

def help_command(update, context):
    update.message.reply_text(
        "Просто напиши любое сообщение, и я его отправлю в Dialogflow!\n"
        "Команды:\n"
        "/start - начать\n"
        "/help - помощь"
    )

def handle_message(update, context):
    user_message = update.message.text
    session_id = str(update.message.chat_id) 
    try:
        reply = detect_intent_texts(project_id, session_id, user_message, language_code)
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("Произошла ошибка при обработке сообщения.")
        print(f"Error: {e}")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    create_intent(project_id)