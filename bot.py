from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow_v2 as dialogflow
import os
from create_intent import detect_intent_texts
from dotenv import load_dotenv


def start(update, context):
    update.message.reply_text("Привет! Я бот, созданный при поддержке DialogFlow)")


def help_command(update, context):
    update.message.reply_text(
        "Просто напиши любое сообщение, и я его отправлю в Dialogflow!\n"
        "Команды:\n"
        "/start - начать\n"
        "/help - помощь"
    )


def handle_message(update, context, project_id):
    tg_session_id = f"tg_{update.effective_chat.id}"
    dialogflow_response = detect_intent_texts(
        project_id=project_id,
        session_id=tg_session_id,
        user_message=update.message.text,
        language_code='ru'
        )
    text = dialogflow_response.query_result.fulfillment_text
    update.message.reply_text(text=text)


def main():
    load_dotenv()
    BOT_TOKEN = os.environ['BOT_TOKEN']
    credential_path = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
    project_id = os.environ['PROJECT_ID']

    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()