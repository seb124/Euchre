from abc import abstractmethod
from classes.cards import Card


class Player:
    def __init__(self, number):
        self.number = number
        self.name = 'Player' + str(number)
        self.hand: list[Card] = []
        self.card_values = [0, 0, 0, 0]
        self.tricks_won = 0

    @abstractmethod
    def evaluate_cards(self):
        pass

    @abstractmethod
    def order_up_card(self, suit: str, flipped_c: Card, dealer):
        pass

    @abstractmethod
    def choose_call_suit(self, suit: str, flipped_c: Card):
        pass   

    @abstractmethod
    def must_call_suit(self, suit: str, flipped_c: Card):
        pass   

    @abstractmethod
    def drop_card(self, flipped_c: Card, caller):
        pass   

    @abstractmethod
    def lead_card(self):
        pass   

    @abstractmethod
    def follow_suit(self, lead_c: Card, played: list[Card]):
        pass  

    @abstractmethod
    def choose_suit(self):
        pass

    @abstractmethod
    def play_clincher(self, played: list[Card], calling_player):
        pass    

    @abstractmethod
    def discard_bad_card(self, suit: str):
        pass   

    @abstractmethod
    def choose_card(self):
        pass   

class Team:
    # Teams are made up of 2 players. In real Euchre, teammates sit across the table from each other. So odd players
    # make up team1, and even numbered players make up team2
    def __init__(self, player_a, player_b, points, tricks):
        self.player_a = player_a
        self.player_b = player_b
        self.points = points
        self.tricks = tricks