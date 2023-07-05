import pandas as pd
import json

import requests


def api_call(name: str, message: str, messageHist: list):
    url = "https://text-lexi-xbuls6ziyq-uc.a.run.app"

    payload = json.dumps({
        "name": name,
        "message": message,
        "history": messageHist
    })

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()

    return response_data.get('message', '')

input_file = "csv_archive/personality.csv"

ouput = input_file.replace("csv_archive/", "tests/")
# load csv
df = pd.read_csv(input_file)
df = df.drop(columns=['Unnamed: 3'])
df['api_response'] = ''
name="Saul"

# iterate over the rows
for index, row in df.iterrows():
    history_dict = json.loads(row['messageHist'])
    # get the list from the dict
    history_list = history_dict['History']
    request = row['request']
    # Call the API
    response = api_call(name, request, history_list)
    df.at[index, 'api_response'] = response

# Save the dataframe to a new csv file
df.to_csv(ouput, index=False)

token = "6185686378:AAHrt6ldLSf7v8mArkmKM9OqhpF1iUwZ2Vk";



