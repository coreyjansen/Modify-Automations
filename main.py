import yaml
import json
import openai
import os
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Set OPENAI_API_KEY env-var before running.")


def generate_description(client, automation, previous_titles):
    """
    Use GPT-4-turbo to generate a new description based on the automation's triggers and actions.
    """
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant that returns JSON with two keys: "
                       "'title' and 'description'. "
                       "Title must follow exactly this template: "
                       "'<Room / Area> – <Trigger> – <Action>'. "
                       "Keep it ≤ 80 characters, title-case every main word, avoid punctuation beside dashes. "
                       "Description is a one-sentence plain-English summary starting with a verb. "
                       "Do not invent functionality not present in the YAML. "
        }
    ]

    # Add previous titles as examples. Feel free to remove this if it is not working as you want but helps keep the titles consistent
    previous_titles_prompt = {
        "role": "system",
        "content": "PREVIOUS TITLES:\n" + "\n".join(previous_titles)
    }
    conversation.append(previous_titles_prompt)

    conversation.append({
        "role": "user",
        "content": f"AUTOMATION CURRENT YAML: {automation}"
    })

    response = client.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=conversation,
        response_format={ "type": "json_object" },
        temperature= 0.0
    )

    assistant_message = json.loads(response.choices[0].message.content)
    while assistant_message["title"] in previous_titles:
        assistant_message["title"] += " (alt)"
    return assistant_message

def process_automations(file_path):
    """
    Process the automations.yaml file, updating titles and descriptions.
    """
    #use this if not using an environment variable for openai api key
    #openai.api_key = 'your_openai_api_key_here'

    client = openai

    previous_titles = []

    # Load YAML file
    with open(file_path, 'r') as file:
        automations = yaml.safe_load(file)

    # Process each automation
    for automation in automations:
        description = generate_description(client, automation, previous_titles)
        previous_titles.append(description["title"])

        print("===== PREVIOUS =====")
        print(automation['alias'])
        print("===== NEW =====")
        print(description["title"])
        print(description["description"])
        print("")

        automation['alias'] = description["title"]
        automation['description'] = description["description"]

    with open(file_path, "w") as f:
        yaml.safe_dump(automations, f, sort_keys=False, allow_unicode=True)

# Set your OpenAI API key

# Path to your automations.yaml file
file_path = 'automations.yaml'
process_automations(file_path)
