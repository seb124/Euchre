import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.computer import Computer
from classes.cards import Card
from classes.player import Player

class AIV1(Computer):
    # update functions as needed - for example, change the order_up_card function to change how this AI behaves when its called in engine.py
    # right now, it's the exact same as the Naive AI "Computer" class

    POINTS_TO_CALL_SUIT = 30
    # At the start of each round, initialize the PT for each player
    def __init__(self, number):
        super().__init__(number)
        
        # Probability table for opponents (keys: player numbers, values: probability distributions)
        self.PT = {
            2: [1/3 for _ in range(24)],  # Equal probability distribution initially
            3: [1/3 for _ in range(24)],
            4: [1/3 for _ in range(24)]
        }

    def update_probability_table(self, player_num: int, action: str, trump_suit: str):
        """
        Update probability table when a player passes or calls trump.
        
        player_num: The player who made the decision (2, 3, or 4)
        action: "pass" or "call"
        trump_suit: The suit in question (e.g., "Spades")
        """
        # Indices for all 8 trump suit cards in the probability table
        trump_cards_indices = [0, 1, 2, 3, 4, 5, 6, 7]  # Jack of Trump, Jack of Off-Suit, A, K, Q, J, 10, 9
        
        top_5_trump_indices = trump_cards_indices[:5]  

        #Ensure no opponent has AI's cards
        for p in self.PT:  
            if p != self.number:  
                removed_prob = 0  # Track total probability removed
                count_unknown_cards = 0  # Count cards that can receive redistributed probability

                for card_idx, card in enumerate(self.hand):  # Check each card in AI's hand
                    removed_prob += self.PT[p][card_idx] 
                    self.PT[p][card_idx] = 0  # No one else can have AI's cards

                #Redistribute probability to remaining unknown cards
                for idx in range(len(self.PT[p])):
                    if self.PT[p][idx] > 0:  # Count valid (unknown) cards
                        count_unknown_cards += 1

                if count_unknown_cards > 0: 
                    redistribute_value = removed_prob / count_unknown_cards  # Evenly distribute lost probability
                    for idx in range(len(self.PT[p])):
                        if self.PT[p][idx] > 0:
                            self.PT[p][idx] += redistribute_value 

        # Adjust Probabilities
        if action == "pass":
            # Player is less likely to have top trump cards
            for idx in top_5_trump_indices:
                self.PT[player_num][idx] *= 0.2  # Reduce their prob

            # Distribute missing probability to other players (only top 5 cards)
            redistribute_amount = sum(self.PT[player_num][idx] for idx in top_5_trump_indices) / 2  
            for p in self.PT:
                if p != player_num:
                    for idx in top_5_trump_indices:
                        self.PT[p][idx] += redistribute_amount / 2

        elif action == "call":
            # Player is more likely to have top trump cards
            for idx in top_5_trump_indices:
                self.PT[player_num][idx] *= 1.5  # Increase their prob

            # Reduce probability of others having these trump cards
            for p in self.PT:
                if p != player_num:
                    for idx in top_5_trump_indices:
                        self.PT[p][idx] *= 0.5  # Reduce their prob

        # ensure prob sum up to 1
        for p in self.PT:
            total = sum(self.PT[p])
            if total > 0:
                self.PT[p] = [x / total for x in self.PT[p]]  # Normalize probabilities



    
    def order_up_card(self, suit: str, flipped_c: Card, dealer: Player, testing: bool):
        """
        Determines whether the AI should order the dealer to pick up the card.
        Updates probability tables based on the AI's decision.
        """
        suit_dict = {'Clubs': 0, 'Diamonds': 1, 'Hearts': 2, 'Spades': 3}
        suit_idx = suit_dict.get(flipped_c.suit)

        if self.card_values[suit_idx] >= self.POINTS_TO_CALL_SUIT:
            suit = flipped_c.suit
            was_card_picked_up = True
            caller = self
            dealer.drop_card(flipped_c, self)
            
            # Update probabilities: AI is more likely to have strong trump cards
            for player in self.PT:
                self.update_probability_table(player, "call", flipped_c.suit)
        
        else:
            was_card_picked_up = False
            caller = None
            not testing and print(f'{self.name}: Pass')

            # Update probabilities: AI is less likely to have strong trump cards
            for player in self.PT:
                self.update_probability_table(player, "pass", flipped_c.suit)

        return self, suit, was_card_picked_up, dealer, caller