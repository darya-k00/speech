import json
import os
from google.cloud import dialogflow_v2 as dialogflow
from dotenv import load_dotenv
import argparse

BASE_DIR = os.path.dirname(__file__)


def get_intents():
    with open(path_to_intents, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return json.loads(file_content)


def create_intent(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    intents_json = get_intents()
    responses = []

    for display_name, items in intents_json.items():
        training_phrases_parts = items.get('questions', [])
        message_texts = [items.get('answer', '')]

        training_phrases = []
        for part in training_phrases_parts:
            training_phrases.append(
                dialogflow.Intent.TrainingPhrase(
                    parts=[dialogflow.Intent.TrainingPhrase.Part(text=part)]
                )
            )

        text = dialogflow.Intent.Message.Text(text=message_texts)
        message = dialogflow.Intent.Message(text=text)

        intent = dialogflow.Intent(
            display_name=display_name,
            training_phrases=training_phrases,
            messages=[message]
        )

        response = intents_client.create_intent(
            request={"parent": parent, "intent": intent}
        )
        responses.append(response)

    return responses


def detect_intent_texts(project_id, session_id, user_message, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=user_message,
        language_code=language_code
        )
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Укажите путь к файлу с данными')
    parser.add_argument('--path', type=str, default=os.path.join(BASE_DIR, 'questions.json'), help='Путь к файлу с данными')
    args = parser.parse_args()
    path_to_intents = args.path
    project_id = os.environ['PROJECT_ID']
    intents_items = get_intents()

    responses = create_intent(project_id, intents_items)
    if responses:
        print(f"Intent created: {responses}")
