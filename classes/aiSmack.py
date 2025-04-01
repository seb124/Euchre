import sys
import os
from openai import OpenAI
import json
from termcolor import colored
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.aiv4 import AIV4
from classes.cards import Card


class AISmack(AIV4):
    """
    AISmack inherits from AIV4. The added functionality to AIVSmack is the LM Studio smack-talking functionality. 
    The local model takes in the probability table and most recent action in and formulates a response based on these inputs. 
    """
    def __init__(self, number):
        super().__init__(number)
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

    
    def generate_smack_talk(self, action: str, flipped_c: Card):

        pt_str = json.dumps(self.PT, indent=2)

        completion = self.client.chat.completions.create(model = "llama-3.2-1b-instruct",
        messages = [
            {"role": "system", "content": 
                "You are an expert in the card game Euchre. The rules are here: https://bicyclecards.com/how-to-play/euchre/. The flipped card, displayed on the table, is " + flipped_c.card_string + ". You are playing against another team and the game is intense. Only respond in one (1) sentence. I will provide a probability table of players' cards and the most recent player action. Base the severity of your trash talk on players' probabilities, but never specifically say the values. Never say a specific percentage."},
            {"role": "user", "content": "Trash talk other players.  Probability Table: " + pt_str + "\nAction: " + action}
        ])
        print(colored(f'{self.name}: {completion.choices[0].message.content}', 'blue'))
