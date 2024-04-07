import yaml
import json
import openai


def generate_description(client, automation, previous_titles):
    """
    Use GPT-4-turbo to generate a new description based on the automation's triggers and actions.
    """
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant who generates titles and descriptions for home automation tasks. "
                       "You will return a json object with the properties title and description. "
                       "Titles should be formatted with the following schema: "
                       "'Specific Area / Room of House Automation Takes Place - What Triggers The Automation - What The Automation Does'. "
                       "If the automation is within a room within a room, mention where in the house that inner room is. "
                       "For example, the Specific Area / Room of the house should be Front Door Closet"
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

        # Save modified YAML file
        with open(file_path, 'w') as file:
            yaml.safe_dump(automations, file)

# Set your OpenAI API key

# Path to your automations.yaml file
file_path = 'automations.yaml'
process_automations(file_path)