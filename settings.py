import json

def load_settings(pi_name, filePath='settings.json'):
    with open(pi_name + "/" + filePath, 'r') as f:
        return json.load(f)