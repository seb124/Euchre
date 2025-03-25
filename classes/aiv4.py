import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.aiv3 import AIV3
import openai
import json
from termcolor import colored

class AIV4(AIV3):
    def generate_smack_talk(self, action: str):
        openai.api_base = "http://localhost:1234/v1"
        openai.api_key = ""

        pt_str = json.dumps(self.PT, indent=2)

        completion = openai.ChatCompletion.create(
        model = "local-model",
        messages = [
            {"role": "system", "content": 
                "You are an expert in the card game Euchre. You are playing against another team and the game is intense. Only respond in one (1) sentence. I will provide a probability table of players' cards and the most recent player action. Base the severity of your trash talk on players' probabilities, but never specifically say the values. Never say a specific percentage."},
            {"role": "user", "content": "Trash talk other players. Probability Table: " + pt_str + "\nAction: " + action}
        ]
        )
        print(colored(f'{self.name}: {completion["choices"][0]["message"]["content"]}', 'blue'))
