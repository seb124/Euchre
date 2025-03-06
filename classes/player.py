from abc import abstractmethod
from classes.cards import Card, Deck


class Player:
    def __init__(self, number):
        self.number = number
        self.name = 'Player' + str(number)
        self.hand: list[Card] = []
        self.card_values = [0, 0, 0, 0]
        self.tricks_won = 0

    def assign_left_bower(self, best: str):
    # This will assign the 'Correct' suit to the odd jack. it always acts as the other suit of the same color
    # Other names for odd jack: left bower

        for c in self.hand:
            if best == 'Clubs' and c.card_string == 'Jack of Spades':
                c.left_bower = True
                c.left_bower_suit = 'Clubs'

            elif best == 'Diamonds' and c.card_string == 'Jack of Hearts':
                c.left_bower = True
                c.left_bower_suit = 'Diamonds'

            elif best == 'Hearts' and c.card_string == 'Jack of Diamonds':
                c.left_bower = True
                c.left_bower_suit = 'Hearts'

            elif best == 'Spades' and c.card_string == 'Jack of Clubs':
                c.left_bower = True
                c.left_bower_suit = 'Spades'

    def assign_clincher(self, best: str):
        for c in self.hand:
            if c.get_suit() == best or c.is_left_bower():
                c.clincher = True

    def assign_points(self, best: str, lead: Card):
        pass

    def evaluate_cards(self):
        pass

    def order_up_card(self, suit: str, flipped_c: Card, dealer):
        pass

    def choose_call_suit(self, suit: str, flipped_c: Card):
        pass   

    def must_call_suit(self, suit: str, flipped_c: Card):
        pass   

    def drop_card(self, flipped_c: Card, caller):
        pass   

    def lead_card(self):
        pass   

    def follow_suit(self, lead_c: Card, played: list[Card]):
        pass  

    def choose_suit(self):
        pass

    def play_clincher(self, played: list[Card], calling_player):
        pass    

    def discard_bad_card(self, suit: str):
        pass   

    def choose_card(self):
        pass   

    def update_probability_table(self, player_num: int, action: str, trump_suit: str):
        pass

    def reset_probability_table(self, deck: Deck):
        pass

class Team:
    # Teams are made up of 2 players. In real Euchre, teammates sit across the table from each other. So odd players
    # make up team1, and even numbered players make up team2
    def __init__(self, player_a, player_b, points, tricks):
        self.player_a = player_a
        self.player_b = player_b
        self.points = points
        self.tricks = tricks