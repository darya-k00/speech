import json
import os
from google.cloud import dialogflow

BASE_DIR = os.path.dirname(__file__)


def get_intents():
    path_to_intents = os.path.join(BASE_DIR, 'questions.json')
    with open(path_to_intents, 'r', encoding='utf-8') as file:
        file_content = file.read()
    return json.loads(file_content)


def create_intent(project_id):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    intents_json = get_intents()

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

        print("Intent created: {}".format(response))