import os
import requests
from time import sleep
import logging
import argparse
import sys
import promptHandler


endpoint_id = "9lfp36qd9tdida"
api_key ="QIOJEYZ74ODYVC4CV7H98XELXVAQR8SWIU2HCZV4"
URI = f"https://api.runpod.ai/v2/{endpoint_id}/run"


def run(prompt, stream=False):
    request = {
        'prompt': prompt,
        'max_new_tokens': 1800,
        'temperature': 0.7,
        'top_k': 50,
        'top_p': 0.7,
        'repetition_penalty': 1.2,
        'batch_size': 8,
        'stream': stream
    }

    response = requests.post(URI, json=dict(input=request), headers={
        "Authorization": f"Bearer {api_key}"
    })

    if response.status_code == 200:
        data = response.json()
        task_id = data.get('id')
        return stream_output(task_id, stream=stream)


def stream_output(task_id, stream=False):
    try:
        url = f"https://api.runpod.ai/v2/{endpoint_id}/stream/{task_id}"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        previous_output = ''

        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if stream:
                    if len(data['stream']) > 0:
                        new_output = data['stream'][0]['output']

                        sys.stdout.write(new_output[len(previous_output):])
                        sys.stdout.flush()
                        previous_output = new_output
                elif len(data['stream']) > 0:
                    return data['stream'][0]['output']

                if data.get('status') == 'COMPLETED':
                    break

            elif response.status_code >= 400:
                logging.error(response.json())
            # Sleep for 0.1 seconds between each request
            sleep(0.1 if stream else 0.5)
    except Exception as e:
        print(e)
        cancel_task(task_id)


def cancel_task(task_id):
    url = f"https://api.runpod.ai/v2/{endpoint_id}/cancel/{task_id}"
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.get(url, headers=headers)
    return response


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runpod AI CLI')
    parser.add_argument('-s', '--stream', action='store_true', help='Stream output')

    prompt = promptHandler.prompt2
    print(run(prompt, stream=parser.parse_args().stream))







