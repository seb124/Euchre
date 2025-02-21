from classes.cards import Card
from classes.computer import Computer
from classes.player import Player


class AIV1(Computer):
    # update functions as needed - for example, change the order_up_card function to change how this AI behaves when its called in engine.py
    # right now, it's the exact same as the Naive AI "Computer" class

    # Assuming the probaility tables will be labeled like pT1, pT2, pT3, pT4, this should be good
    def order_up_card(self, suit: str, flipped_c: Card, dealer: Player, testing: bool):
        high_value_cards = self.get_high_value_cards(self.hand, suit)
        teammate_trump_prob = sum(pT3[card] for card in high_value_cards)
        opponent_trump_prob = sum(pT2[card] for card in high_value_cards) + sum(pT4[card] for card in high_value_cards)

        picked_value = self.eval_trump_choice(teammate_trump_prob, opponent_trump_prob, suit)
        passed_value = self.eval_alternative(flipped_c, self.hand)

        if picked_value >= passed_value: # Can potentially play around with >= or >
            suit = flipped_c.suit
            was_card_picked  = True
            caller = self
            dealer.drop_card(flipped_c, self)
        else:
            was_card_picked = False
            caller = None
            not testing and print(f'{self.name}: Pass')
        return self, suit, was_card_picked, dealer, caller
    
    def get_high_value_cards(hand, suit):
        high_value_cards = []
        for card in hand:
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
                + (teammate_trump_prob * self.calculate_bonus_penalty(teammate_trump_prob)) 
                - (opponent_trump_prob * self.calculate_bonus_penalty(opponent_trump_prob)))

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
    
    def calculate_bonus_penalty(probability):
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
            high_value_cards = self.get_high_value_cards(hand, suit)
            teammate_trump_prob = sum(pT3[card] for card in high_value_cards)
            opponent_trump_prob = sum(pT2[card] for card in high_value_cards) + sum(pT4[card] for card in high_value_cards)

            value = (self.card_weight(suit) 
                + (teammate_trump_prob * self.calculate_bonus_penalty(teammate_trump_prob)) 
                - (opponent_trump_prob * self.calculate_bonus_penalty(opponent_trump_prob)))

            if value > best_alternative_val:
                best_alternative_val = value
                best_suit = suit

        return best_alternative_val