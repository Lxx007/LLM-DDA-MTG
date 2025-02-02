import os
import openai
from openai import OpenAI
import time
import random
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-4o'
OPENAI_RATE_LIMIT = 0.6
openai.api_key = API_KEY

def get_chat_response(gm_setting: str, prompt: str, model= 'gpt-4o') :

    #print("Initiated chat with OpenAI API.")
    client = OpenAI()
    start_time = time.perf_counter()
    completion = client.chat.completions.create(model=model,
                                                messages=[
                                                    {"role": "system", "content": gm_setting},
                                                    {"role": "user", "content": prompt}],
                                                temperature = 0)
    #print("Completed chat with OpenAI API.")
    return completion.choices[0].message.content, model
