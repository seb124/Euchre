import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.computer import Computer
from classes.cards import Card
from classes.player import Player
from classes.cards import Deck


class AIV3(Computer):
    # At the start of each round, initialize the PT for each player
    def __init__(self, number):
        super().__init__(number)
        deck = Deck()
        card_list = deck.build()

        # Probability table for opponents
        self.PT: dict[int, dict[str, float]] = {
            player: {card.card_string: 1/3 for card in card_list}  # Equal probability distribution initially
            for player in [1, 2, 3, 4] if player != self.number
        }

    def update_probability_table(self, player_num: int, action: str, flipped_card: Card):
        """
        Update probability table when a player passes or calls trump.
        
        player_num: The player who made the decision (1, 2, 3, or 4)
        action: "pass" or "call"
        trump_suit: The suit in question (e.g., "Spades")
        """
        off_suit = {"Spades": "Clubs", "Clubs": "Spades", "Diamonds": "Hearts", "Hearts": "Diamonds"}

        # Indices for all 8 trump suit cards in the probability table
        trump_cards = [f"Jack of {flipped_card.suit}", 
                               f"Jack of {off_suit[flipped_card.suit]}", 
                               f"Ace of {flipped_card.suit}", 
                               f"King of {flipped_card.suit}", 
                               f"Queen of {flipped_card.suit}", 
                               f"10 of {flipped_card.suit}", 
                               f"9 of {flipped_card.suit}"]  # Jack of Trump, Jack of Off-Suit, A, K, Q, 10, 9
        
        top_5_trump_cards = trump_cards[:5]

        trump_reduction_factors = { #sets up what to reduce by
            f"Jack of {flipped_card.suit}": 0.7,  # Right Bower
            f"Jack of {off_suit[flipped_card.suit]}": 0.7,  # Left Bower
            f"Ace of {flipped_card.suit}": 0.6,
            f"King of {flipped_card.suit}": 0.5,
            f"Queen of {flipped_card.suit}": .4
        }

        #Ensure no opponent has AI's cards
        for p in self.PT.keys():  
            removed_prob = 0  # Track total probability removed
            count_unknown_cards = 0  # Count cards that can receive redistributed probability

            for card in self.hand:  # Check each card in AI's hand
                removed_prob += self.PT[p][card.card_string]
                self.PT[p][card.card_string] = 0  # No one else can have AI's cards

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
        #double check that it all adds up 
        for p in self.PT:
            total = sum(self.PT[p][card] for card in self.PT[p])
            if total > 0:
                for card in self.PT[p]:
                    self.PT[p][card] /= total  
                    
    def reset_probability_table(self, deck):
        card_list = deck.cards
        self.PT: dict[int, dict[str, float]] = {
            player: {card.card_string: 1/3 for card in card_list}  # Equal probability distribution initially
            for player in [1, 2, 3, 4] if player != self.number
        }

    def order_up_card(self, suit: str, flipped_c: Card, dlr_index: int, dealer: Player, testing: bool):
        teammate_number = ((self.number + 1) % 4) + 1
        opponent_numbers = [p for p in [1, 2, 3, 4] if p not in [self.number, teammate_number]]
        high_value_cards = self.get_high_value_cards(flipped_c.suit)
        teammate_trump_prob = sum(self.PT[teammate_number][card] for card in high_value_cards)
        opponent_trump_prob = sum(self.PT[opponent_numbers[0]][card] for card in high_value_cards) + sum(self.PT[opponent_numbers[1]][card] for card in high_value_cards)

        picked_value = self.eval_trump_choice(teammate_trump_prob, opponent_trump_prob, flipped_c.suit)
        passed_value = self.eval_alternative(flipped_c.suit)

        adjustment = self.consider_turn_order(dlr_index)

        if (picked_value + adjustment) > (passed_value):
            suit = flipped_c.suit
            was_card_picked  = True
            caller = self
            dealer.drop_card(flipped_c, self)
        else:
            was_card_picked = False
            caller = None
            not testing and print(f'{self.name} passed on calling {flipped_c.suit} as the trump suit.')
        return self, suit, was_card_picked, dealer, caller
    
    def get_high_value_cards(self, suit):
        high_value_cards = []
        for card in self.hand:
            if suit == "Clubs" and (card.card_string == "Jack of Clubs" or "Jack of Spades" or "Ace of Clubs" or "King of Clubs" or "Queen of Clubs"):
                high_value_cards.append(card.card_string)
            elif suit == "Spades" and (card.card_string == "Jack of Clubs" or "Jack of Spades" or "Ace of Spades" or "King of Spades" or "Queen of Spades"):
                high_value_cards.append(card.card_string)
            elif suit == "Diamonds" and (card.card_string == "Jack of Diamonds" or "Jack of Hearts" or "Ace of Diamonds" or "King of Diamonds" or "Queen of Diamonds"):
                high_value_cards.append(card.card_string)
            elif suit == "Hearts" and (card.card_string == "Jack of Diamonds" or "Jack of Hearts" or "Ace of Hearts" or "King of Hearts" or "Queen of Hearts"):
                high_value_cards.append(card.card_string)

        return high_value_cards
    
    def eval_trump_choice(self, teammate_trump_prob, opponent_trump_prob, suit):
        return self.card_weight(suit) + (teammate_trump_prob * self.calculate_bonus_penalty(teammate_trump_prob)) - (opponent_trump_prob * self.calculate_bonus_penalty(opponent_trump_prob))
    
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
        if probability > 0.75:  # Adjusting threshold slightly
            return 12  # Increase penalty for high opponent trump probability
        elif probability > 0.5:
            return 6  # Increase this slightly
        else:
            return 0
    
    def eval_alternative(self, suit):
        best_alternative_val = 0

        for suit_type in ["Clubs", "Spades", "Diamonds", "Hearts"]:
            if suit_type is suit:
                continue

            teammate_number = ((self.number + 1) % 4) + 1
            opponent_numbers = [p for p in [1, 2, 3, 4] if p not in [self.number, teammate_number]]
            high_value_cards = self.get_high_value_cards(suit)
            teammate_trump_prob = sum(self.PT[teammate_number][card] for card in high_value_cards)
            opponent_trump_prob = sum(self.PT[opponent_numbers[0]][card] for card in high_value_cards) + sum(self.PT[opponent_numbers[1]][card] for card in high_value_cards)
            
            value = self.eval_trump_choice(teammate_trump_prob, opponent_trump_prob, suit_type)

            if value > best_alternative_val:
                best_alternative_val = value

        return best_alternative_val
    
    def consider_turn_order(self, dlr_index):
        position_adjustment = {0: -3, 1: 3, 2: -2, 3: 6}
        player_order = [(dlr_index) % 4 + 1, (dlr_index + 1) % 4 + 1, (dlr_index + 2) % 4 + 1, dlr_index]
        return position_adjustment[player_order.index(self.number)]