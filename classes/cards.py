import random
from termcolor import colored


class Card:
    def __init__(self, suit, rank, point, left_bower, left_bower_suit, owner, display, card_string, clincher=False):
        self.suit = suit
        self.rank = rank
        self.point = point
        self.left_bower = left_bower
        self.left_bower_suit = left_bower_suit
        self.owner = owner
        self.display = display
        self.card_string = card_string
        self.clincher = clincher

    def show(self):
        if self.suit == 'Clubs':
            self.display = colored(f'{self.rank} ♣ Clubs', 'grey', 'on_white')
        elif self.suit == 'Spades':
            self.display = colored(f'{self.rank} ♠ Spades', 'grey', 'on_white')
        elif self.suit == 'Hearts':
            self.display = colored(f'{self.rank} ♥ Hearts', 'red', 'on_grey')
        elif self.suit == 'Diamonds':
            self.display = colored(f'{self.rank} ♦ Diamonds', 'red', 'on_grey')

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_point(self):
        # This is used to determine the best card played each trick
        return self.point

    def get_clincher(self):
        # Boolean so computer players know which cards are clincher
        return self.clincher

    def is_left_bower(self):
        # Boolean that is true for the jack that 'switches suit' each round and becomes a clincher
        return self.left_bower

    def suit_left_bower(self):
        # The effective suit of each card. The only change from the original suit is the odd jack card aka left bower
        # This counts as the other suit of the same color (diamonds and hearts are red, spades and clubs are black)
        return self.left_bower_suit


class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.build()

    def __len__(self):
        return len(self)  # Shows how many cards are in deck. This should be 24 for 9 -> Ace

    def show(self):
        for c in self.cards:
            c.show()

    def build(self):
        # This creates the deck of 24 cards
        for suit in self.suits:  # for every suit and rank, creates a card that is added to cards list
            for rank in self.ranks:
                card = Card(suit, rank, point=0, clincher=False, left_bower=False, left_bower_suit=suit, owner=None,
                            display='', card_string=f'{rank} of {suit}')
                self.cards.append(card)
        return self.cards

    def destroy(self):
        # This empties out the cards in the deck. Used at the end of each round to help simulate reshuffling
        self.cards = []

    def deal_cards(self, player_name):
        # Deals 5 random cards to each player
        for i in range(5):
            random_card = random.choice(self.cards)
            self.cards.remove(random_card)
            player_name.hand.append(random_card)
        return player_name.hand

    def flip_card(self):
        # Flips one card on the table. Players have option to tell dealer to pick up this card to make its suit clincher
        # This is called after all players have 5 cards
        flipped = random.choice(self.cards)
        return flipped
