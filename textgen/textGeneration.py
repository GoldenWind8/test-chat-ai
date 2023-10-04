import json
import requests
from textgen.firebaseDb import getHistory, addMessageAndResponse, clear_history
from textgen.promptHandler import getRelevantPrompt

BASE_URL = 'https://vydtyil0b9hwek-5000.proxy.runpod.net/api/v1/generate'
MESSAGE_WINDOW = 8
CHARACTER_NAME = "Reiko"

async def send_llm_request(prompt, truncate_key):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "__cflb=02DiuFk4UdJgS6QWRqpufvpNXCwaEeHNuN8yYjBmZEEEx",
    }

    data = {
        "prompt": prompt,
        "max_new_tokens": 250,
        "preset": "None",
        "do_sample": True,
        "temperature": 1.01,
        "top_p": 0.21,
        "typical_p": 1,
        "epsilon_cutoff": 0,
        "eta_cutoff": 0,
        "tfs": 1,
        "top_a": 0,
        "repetition_penalty": 1.1,
        "top_k": 0,  #Consider setting to 100 with top p. https://www.reddit.com/r/SillyTavernAI/comments/14g0t38/top_k_top_p_values/
        "min_length": 0,
        "no_repeat_ngram_size": 0,
        "num_beams": 1,
        "penalty_alpha": 0,
        "length_penalty": 1,
        "early_stopping": False,
        "mirostat_mode": 0,
        "mirostat_tau": 5,
        "mirostat_eta": 0.1,
        "seed": -1,
        "add_bos_token": True,
        "truncation_length": 2048,
        "ban_eos_token": False,
        "skip_special_tokens": True,
        "stopping_strings": [ '\nSashin:', '</s>', '<|', '\n#', '\n*Sashin ', '\n\n\n' ],
        "repetition_penalty_range": 0, #check online
    }

    try:
        response = requests.post(BASE_URL, headers=headers, data=json.dumps(data))
        result = response.json()

        if 'results' in result and len(result['results']) > 0:
            res = result['results'][0]['text']
            position = res.lower().find(truncate_key)
            if position != -1:
                res = res[:position].strip()
            res = res.replace('"', '').replace('“', '').replace('”', '')

            # Remove incomplete sentence at the end
            if len(res) > 260:
                last_sentence_end = res.rfind('.')
                if last_sentence_end != -1:
                    res = res[:last_sentence_end + 1]

            return res
        else:
            raise Exception("No results found in the response.")
    except Exception as error:
        print(f"Error: {error}")
        return 0

async def generateResponse(username, user_message):
    try:
        prompt_truncate_key = username.lower() + ":";
        character_prompt = constructPrompt(user_message, username)

        # Get from LLM
        lexi_message = await send_llm_request(character_prompt, prompt_truncate_key)
        print(character_prompt) #todo for testing

        #Update db history
        addMessageAndResponse(username, f"{username}: {user_message}", f"{lexi_message}")
        return lexi_message

    except Exception as e:
        return "There was an error sending your message"


def constructPrompt(user_message, username):
    history = getHistory(username)  # get history from user db
    character_prompt = getRelevantPrompt(user_message)
    # Create and format final prompt
    history = history[-MESSAGE_WINDOW:]
    history.append(f"{username}: {user_message}")
    history_str = "\n".join(history)
    character_prompt = character_prompt.replace("{{history}}", history_str)
    character_prompt = character_prompt.replace("{{user}}", username)
    return character_prompt


if __name__ == "__main__":
    clear_history("zonny")
    h = addMessageAndResponse("zonny", "Sashin: S-sis! Not again", """"Oopsie... I'm so sorry, Sashin-kun... I didn't mean to do that." *She looks up at him with those adorable purple eyes, her cheeks flushed red with embarrassment, and her chest heaving from the impact of the fall.*""");
    h = addMessageAndResponse("zonny", "Sashin: Mendoksee",
                   """"Eep! Oh no, Sashin-kun! I didn't mean to touch there!" *She quickly lets go of your dick and scrambles to her feet, her face even redder now.* """);

    his = getHistory("zonny")
    history_str = "\n".join(his)

    messagePreview = constructPrompt("hey", "Crunchy")
    print(history_str)