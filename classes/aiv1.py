import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.computer import Computer
from classes.cards import Card
from classes.player import Player
from classes.cards import Deck


class AIV1(Computer):
    # At the start of each round, initialize the PT for each player
    def __init__(self, number):
        super().__init__(number)
        deck = Deck()
        card_list = deck.build()

        # Probability table for opponents (keys: player numbers, values: probability distributions)
        self.PT = {
            player: {card: 1/3 for card in card_list}  # Equal probability distribution initially
            for player in [1, 2, 3, 4] if player != self.number
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
        teammate_number = ((self.number + 1) % 4) + 1
        opponent_numbers = [p for p in [1, 2, 3, 4] if p not in [self.number, teammate_number]]
        high_value_cards = self.get_high_value_cards(suit)
        teammate_trump_prob = sum(self.PT[teammate_number][card] for card in high_value_cards)
        opponent_trump_prob = sum(self.PT[opponent_numbers[0]][card] for card in high_value_cards) + sum(self.PT[opponent_numbers[1]][card] for card in high_value_cards)

        picked_value = self.eval_trump_choice(teammate_trump_prob, opponent_trump_prob, suit)
        passed_value = self.eval_alternative(flipped_c, self.hand)

        if picked_value > passed_value: # I tried > vs >= and > is muchhhh better than >= actually
            suit = flipped_c.suit
            was_card_picked  = True
            caller = self
            dealer.drop_card(flipped_c, self)
        else:
            was_card_picked = False
            caller = None
            not testing and print(f'{self.name}: Pass')
        return self, suit, was_card_picked, dealer, caller
    
    def get_high_value_cards(self, suit):
        high_value_cards = []
        for card in self.hand:
            if suit == "Clubs":
                if card == "Jack of Clubs" or "Jack of Spades" or "Ace of Clubs":
                    high_value_cards.append(card)
            elif suit == "Spades":
                if card == "Jack of Clubs" or "Jack of Spades" or "Ace of Spades":
                    high_value_cards.append(card)
            elif suit == "Diamonds":
                if card == "Jack of Diamonds" or "Jack of Hearts" or "Ace of Diamonds":
                    high_value_cards.append(card)
            elif suit == "Hearts":
                if card == "Jack of Diamonds" or "Jack of Hearts" or "Ace of Hearts":
                    high_value_cards.append(card)
        
        return high_value_cards
    
    def eval_trump_choice(self, teammate_trump_prob, opponent_trump_prob, suit):
        return (self.card_weight(suit) 
                + teammate_trump_prob * self.calculate_bonus_penalty(teammate_trump_prob)
                - (opponent_trump_prob * self.calculate_bonus_penalty(opponent_trump_prob)))
    
    def evaluate_cards(self):
        return super().evaluate_cards()

    def card_weight(self, suit):
        weights = self.evaluate_cards()
        if suit == "Clubs":
            return weights[0]
        elif suit == "Spades":
            return weights[3]
        elif suit == "Diamonds":
            return weights[1]
        elif suit == "Hearts":
            return weights[2]
        else:
            return 0
    
    def calculate_bonus_penalty(self, probability):
        if probability > 0.8:
            return 10
        elif probability > 0.5:
            return 5
        else:
            return 0
    
    def eval_alternative(self, suit, hand):
        best_alternative_val = 0
        best_suit = None

        for suit_type in ["Clubs", "Spades", "Diamonds", "Hearts"]:
            if suit_type is suit:
                continue

            teammate_number = ((self.number + 1) % 4) + 1
            opponent_numbers = [p for p in [1, 2, 3, 4] if p not in [self.number, teammate_number]]
            high_value_cards = self.get_high_value_cards(suit)
            teammate_trump_prob = sum(self.PT[teammate_number][card] for card in high_value_cards)
            opponent_trump_prob = sum(self.PT[opponent_numbers[0]][card] for card in high_value_cards) + sum(self.PT[opponent_numbers[1]][card] for card in high_value_cards)
            
            value = (self.card_weight(suit) 
                + (teammate_trump_prob * self.calculate_bonus_penalty(teammate_trump_prob)) 
                - (opponent_trump_prob * self.calculate_bonus_penalty(opponent_trump_prob)))

            if value > best_alternative_val:
                best_alternative_val = value
                best_suit = suit

        return best_alternative_val