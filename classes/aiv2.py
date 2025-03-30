import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from classes.aiv1 import AIV1
from classes.cards import Card
from classes.player import Player


class AIV2(AIV1):

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
    
    def consider_turn_order(self, dlr_index):
        position_adjustment = {0: -3, 1: 3, 2: -2, 3: 6}
        player_order = [(dlr_index) % 4 + 1, (dlr_index + 1) % 4 + 1, (dlr_index + 2) % 4 + 1, dlr_index]
        return position_adjustment[player_order.index(self.number)]