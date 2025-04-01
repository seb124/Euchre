import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.aiv2 import AIV2
from classes.cards import Card


class AIV3(AIV2):
    """
    AIV3 inherits from AIV2. AIV3 makes adjustments to update_probability_table. 
    The probability table is updated with a smarter/riskier approach based on inherent the value of the cards.
    """
    def update_probability_table(self, player_num: int, action: str, flipped_c: Card, suit: str):
        # This function updates the probability table when a player passes or calls trump.

        off_suit = {"Spades": "Clubs", "Clubs": "Spades", "Diamonds": "Hearts", "Hearts": "Diamonds"}
        
        trump_reduction_factors = { # sets up what to reduce by. If a player passes, they're much less likely to have the higher cards of that suit
            f"Jack of {suit}": 0.7,  # Right Bower
            f"Jack of {off_suit[suit]}": 0.7,  # Left Bower
            f"Ace of {suit}": 0.6,
            f"King of {suit}": 0.5,
            f"Queen of {suit}": .4
        }

        #Ensure no opponent has AI's cards
        for p in self.PT.keys():  
            removed_prob = 0  
            count_unknown_cards = 0 

            for card in self.hand:  # Check each card in AI's hand
                removed_prob += self.PT[p][card.card_string]
                self.PT[p][card.card_string] = 0  # No one else can have AI's cards

            # No one can have the card on the table in their hand
            removed_prob += self.PT[p][flipped_c.card_string]
            self.PT[p][flipped_c.card_string] = 0

            #Redistribute probability to remaining unknown cards
            for card in self.PT[p].keys():
                if self.PT[p][card] > 0:  # Count valid (unknown) cards
                    count_unknown_cards += 1

            if count_unknown_cards > 0: 
                redistribute_value = removed_prob / count_unknown_cards  # Evenly distribute lost probability
                for card in self.PT[p].keys():
                    if self.PT[p][card] > 0:
                        self.PT[p][card] += redistribute_value

        # Adjust Probabilities
        if action == "pass":
            # Player is less likely to have top trump cards
            removed_prob = 0 #track probability decreases from this player
            
            for card, reduction in trump_reduction_factors.items():
                if card in self.PT[player_num]:  # Ensure the card exists in the table
                    removed_prob += self.PT[player_num][card] * reduction
                    self.PT[player_num][card] *= (1 - reduction) 

            # Redistribute the removed probability to other players
            num_opponents = len(self.PT) - 1
            if num_opponents > 0:
                for p in self.PT:
                    if p != player_num:
                        for card in trump_reduction_factors.keys():
                            self.PT[p][card] += removed_prob / num_opponents  

        elif action == "call":
            increase_factor = 1.5  # Increase probability of having top trump
            for card in trump_reduction_factors.keys():
                if card in self.PT[player_num]:  
                    self.PT[player_num][card] *= increase_factor  

            # Reduce probability of others having these trump cards
            for p in self.PT:
                if p != player_num:
                    for card in trump_reduction_factors.keys():
                        self.PT[p][card] *= 0.5 

            # ensure prob sum up to 1
            for p in self.PT:
                total = sum(self.PT[p][card] for card in self.PT[p])
                if total > 0:
                    for card in self.PT[p]:
                        self.PT[p][card] = self.PT[p][card] / total  # Normalize probabilities