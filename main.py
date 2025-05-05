import yaml
import json
import openai
import os
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("Set OPENAI_API_KEY env-var before running.")


def generate_titles_bulk(client, automations):
    """
    Send *all* automations in one request and get back a JSON object
    mapping each automation's `id` (a.k.a. unique_id) to a new
    { "title": ..., "description": ... } pair.
    """
    system_msg = (
        "You are a helpful assistant analysing *all* Home-Assistant "
        "automations for a household.  Return a single JSON object "
        "whose keys are the automation 'id' values and whose values are "
        "objects containing exactly two keys: 'title' and 'description'. "
        "Title template: '[Area] - [Trigger] - [Action] [Optional: - Context]', "
        "≤80 chars, Title-Case, dash separators only. "
        "Description: one concise sentence starting with a verb. "
        "Do NOT invent features not present in the YAML; ignore disabled "
        "triggers/actions (enabled: false)."
    )

    user_msg = "AUTOMATIONS YAML:\n" + yaml.safe_dump(
        automations, sort_keys=False, allow_unicode=True
    )

    response = client.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
    )
    return json.loads(response.choices[0].message.content)

def process_automations(file_path):
    """
    Process the automations.yaml file, updating titles and descriptions.
    """
    #use this if not using an environment variable for openai api key
    #openai.api_key = 'your_openai_api_key_here'

    client = openai

    # Load YAML file
    with open(file_path, 'r') as file:
        automations = yaml.safe_load(file)

    # Ask GPT for all titles/descriptions at once
    mapping = generate_titles_bulk(client, automations)
    seen_titles = set()

    for automation in automations:
        uid = automation.get("id")  # Home-Assistant’s unique identifier
        if uid not in mapping:
            # skip automations missing an id or unknown to GPT
            continue

        new_title  = mapping[uid]["title"]
        new_desc   = mapping[uid]["description"]

        # insure uniqueness in case GPT produced duplicates
        original_title = new_title
        counter = 2
        while new_title in seen_titles:
            new_title = f"{original_title} ({counter})"
            counter += 1
        seen_titles.add(new_title)

        print(f"{automation.get('alias')}  →  {new_title}")

        automation["alias"]       = new_title
        automation["description"] = new_desc

    with open(file_path, "w") as f:
        yaml.safe_dump(automations, f, sort_keys=False, allow_unicode=True)

# Set your OpenAI API key

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retitle HA automations")
    parser.add_argument("yaml_file", nargs="?", default="automations.yaml")
    args = parser.parse_args()
    process_automations(args.yaml_file)
