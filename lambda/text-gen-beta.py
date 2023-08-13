import asyncio
import json
from promptHandler import getRelevantPrompt
import requests
from firebaseDb import retrieve_validate_history2, add_messages_to_history

BASE_URL = 'https://4j36h5uheycliv-5000.proxy.runpod.net/api/v1/generate'

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

async def lambda_handler(username, name, user_message):
    try:
        history = retrieve_validate_history(username)  #todo get history from user db

        prompt_truncate_key = name.lower() + ":";
        character_prompt = getRelevantPrompt(user_message)

        # Create and format final prompt
        history.append(f"{name}: {user_message}")
        history_str = "\n".join(history)
        character_prompt = character_prompt.replace("$name", name)
        character_prompt = character_prompt.replace("$history", history_str)

        # Final prompt to LLM and store message
        lexi_message = await send_llm_request(character_prompt, prompt_truncate_key)
        history.append(f"Lexi:{lexi_message}")
        print(character_prompt)

        return {
            'statusCode': 200,
            'body': lexi_message
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def retrieve_validate_history(username):
    history = [
        "Stacy: Hey brandy",
        "Brandy: Hey Stacy, how are you?",
        "Stacy: I'm doing great, Brandy! I can't wait to spend some time together tonight. Are you ready for our little adventure?",
        "Brandy: I'm so excited! I've been looking forward to this all week. I can't wait to see what you have planned for us.",
        "Stacy: I'll be wearing a black lace bra and matching thong set that hugs my curves perfectly. My hair will be styled in loose waves around my shoulders, and I'll be wearing a bit of makeup to enhance my natural beauty.",
        "Brandy: oh",
        "Stacy: Stacy hesitates for a moment before slowly lowering herself onto your lap, her hands gently caressing your chest as she looks up at you with a mix of fear and submission in her eyes.*\n\nI... I understand, *she whispers softly,* but please remember that I am still learning about this world.",
];
    return history;



if __name__ == "__main__":
    #loop = asyncio.get_event_loop()
    # Use the event loop to run the async function until it completes
    #result = loop.run_until_complete(lambda_handler("gsdgfj","Brandy", "Oh baby its too much, just get on your knees and suck my cock"))
    #print(result)
    h = add_messages_to_history("zonny", "hety", "bae");
    his = retrieve_validate_history2("zonny")
    print(h)
    print(his)