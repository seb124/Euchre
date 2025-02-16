from abc import abstractmethod
from cards import Card


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
    def pick_up_card(self, suit: str, flipped_c: Card):
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