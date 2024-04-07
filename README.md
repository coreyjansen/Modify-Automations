# Home Automation Description Generator

This Python script leverages OpenAI's GPT models to generate and update titles and descriptions for home automation tasks. It processes an `automations.yaml` file, which contains your home automation configurations, and updates it with newly generated titles and descriptions that are more informative and human-friendly.

## Prerequisites

Before running the script, ensure you have the following prerequisites installed:

- Python 3.8 or newer
- `openai` Python package
- `pyyaml` Python package

You can install the required packages using pip:

```bash
pip install openai pyyaml
```

## Configuration

1. **Set up your OpenAI API key** : The script requires an OpenAI API key to interact with GPT models. You can set your API key as an environment variable:

```bash
export OPENAI_API_KEY='your_api_key_here'
```

1. ** file** : The script expects a YAML file named `automations.yaml` containing your home automation configurations. Ensure this file is in the same directory as the script or provide the path to the file when calling the function.

## Usage

1. **Run the Script** : To run the script, navigate to the directory containing the script and your `automations.yaml` file, then execute:

```bash
python script_name.py
```

Replace `script_name.py` with the name of your Python script file.

1. **Review Updates** : The script will process each automation in your YAML file, generating new titles and descriptions, and updating the file in place. Review the changes to ensure they meet your expectations.

## How It Works

- The script reads your `automations.yaml` file to get the current configurations of your home automations.
- It uses OpenAI's GPT models to generate a new title and description for each automation based on its triggers and actions.
- The new titles and descriptions are formatted to provide clear and concise information about what each automation does and where it is applied.
- Finally, the script updates the `automations.yaml` file with the new titles and descriptions.

## Contributions

Contributions are welcome! If you have suggestions for improvements or encounter any issues, please open an issue or submit a pull request.

```vbnet
Feel free to adjust the guide according to your project's specifics or any additional steps you might require!
```
