import pandas as pd
import requests
import json
from typing import List

def json_str_to_list(json_str: str) -> List[str]:
    return json.loads(json_str)

def api_call(name: str, message: str, history):
    url = "https://text-lexi-xbuls6ziyq-uc.a.run.app"

    payload = json.dumps({
        "name": name,
        "message": message,
        "history": history
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response_data = response.json()

    return response_data.get('message', '')

# Read CSV file
data = pd.read_csv('csv_archive/personality.csv', encoding='latin1')
# Print column names
print(data.columns)
responses = []

for index, row in data.iterrows():
    history_string = row['messageHist']

    # Remove or replace invalid characters
    history_string = history_string.replace('Ã¢Â€Â™', "'")

    # Now evaluate the string
    history = eval(history_string)
    # Call API
    response = api_call('Lexi', row['request'], history)
    responses.append(response)

# Add new column
data['newResponses'] = responses
# Save DataFrame to CSV
data.to_csv('testing.csv', index=False)

