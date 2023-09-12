import json
import requests
from textgen.firebaseDb import getHistory, addMessage
from textgen.promptHandler import getRelevantPrompt

BASE_URL = 'https://q0oiaj3lsv6ppd-5000.proxy.runpod.net/api/v1/generate'
MESSAGE_WINDOW = 8

async def send_llm_request(prompt, truncate_key):
    headers = {
        "Content-Type": "application/json",
        "Cookie": "__cflb=02DiuFk4UdJgS6QWRqpufvpNXCwaEeHNuN8yYjBmZEEEx",
    }

    data = {
        "prompt": prompt,
        "max_new_tokens": 80,
        "preset": "None",
        "do_sample": True,
        "temperature": 0.7,
        "top_p": 0.1,
        "typical_p": 1,
        "epsilon_cutoff": 0,
        "eta_cutoff": 0,
        "tfs": 1,
        "top_a": 0,
        "repetition_penalty": 1.1,
        "top_k": 40,
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
        "stopping_strings": [],
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

async def handlePrompt(username, name, user_message):
    try:
        history = getHistory(username)  #get history from user db

        prompt_truncate_key = username.lower() + ":";
        character_prompt = getRelevantPrompt(user_message)

        # Create and format final prompt
        history = history[-MESSAGE_WINDOW:]
        history.append(f"{username}: {user_message}")
        history_str = "\n".join(history)
        character_prompt = character_prompt.replace("$name", username)
        character_prompt = character_prompt.replace("$history", history_str)

        # Get from LLM
        lexi_message = await send_llm_request(character_prompt, prompt_truncate_key)
        #print(character_prompt) #todo for testing

        #Update db history
        addMessage(username, f"{username}: {user_message}", f"Stacy:{lexi_message}")
        return lexi_message

    except Exception as e:
        return "There was an error sending your message"




if __name__ == "__main__":
    #loop = asyncio.get_event_loop()
    # Use the event loop to run the async function until it completes
    #result = loop.run_until_complete(lambda_handler("gsdgfj","Brandy", "Oh baby its too much, just get on your knees and suck my cock"))
    #print(result)
    h = addMessage("zonny", "hety", "bae");
    his = getHistory("zonny")
    print(h)
    print(his)