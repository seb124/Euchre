import time

from termcolor import colored
from classes.cards import Card
from classes.player import Player
import os
clear = lambda: os.system('clear')

class User(Player):    

    def order_up_card(self, suit: str, flipped_c: Card, dlr_index: int, dealer: Player, testing: bool):
    # This allows the user to tell a player whether to pick up the flipped card and call that suit clincher
        
        time.sleep(1)
        clear()
        options = ['y', 'n']
        print('It\'s your turn. Your hand is: \n')
        for c in self.hand:
            print(c.display)
            time.sleep(0.3)
        time.sleep(0.5)
        print(f'The flipped card is: {flipped_c.display}')
        while True:
            try:
                does_user_order_card = input(
                    f'\n{dealer.name + " is" if dealer is not self else "You are"} the dealer. Would you like{" them" if dealer is not self else ""} to pick up the flipped card? (y/n)')
                if does_user_order_card.lower() not in options:
                    raise TypeError
                if does_user_order_card.lower() == 'y':
                    suit = flipped_c.suit
                    dealer.drop_card(flipped_c, self)
                    was_suit_picked = True
                elif does_user_order_card.lower() == 'n':
                    was_suit_picked = False
                else:
                    print('Invalid Input. Please enter y or n next time')
                return self, suit, was_suit_picked, dealer, self
            except TypeError:
                print('Invalid input. Please enter y or n to determine whether the dealer should pick up the card')

    def choose_call_suit(self, suit: str, flipped_c: Card, testing: bool):
         # This allows the user to determine clincher for that round after everyone has passed on the flipped card

        was_suit_declared = False
        user_call_options = ['y', 'n']
        suit_options = ['c', 'd', 'h', 's']
        suit_options.pop(suit_options.index(flipped_c.suit[0].lower()))
        # This removes the suit of the flipped card. cant be clincher
        print('\n')
        for c in self.hand:
            print(c.display)
        while True:
            try:
                does_user_call = input('\nIt\'s your turn. Your hand is above. Would you like to choose the trump suit? (y/n):')
                if does_user_call[0].lower() not in user_call_options:
                    raise ValueError
                elif does_user_call[0].lower() == 'y':
                    was_suit_declared = True
                    caller = self
                    called_suit = input(f'\nPlease enter the first letter of the suit you\'d like to call '
                                        f'({suit_options[0]}/{suit_options[1]}/{suit_options[2]}): ')
                    suit_letter = called_suit[0].lower()
                    if suit_letter not in suit_options:
                        if suit_letter == flipped_c.suit[0].lower():
                            print(f'\nYou may not call {flipped_c.suit} because it was turned down as the flipped card.')
                        else:
                            pass
                        raise ValueError
                    else:
                        pass
                    if suit_letter == 'c':
                        suit = suit.join('Clubs')
                    elif suit_letter == 'd':
                        suit = suit.join('Diamonds')
                    elif suit_letter == 'h':
                        suit = suit.join('Hearts')
                    elif suit_letter == 's':
                        suit = suit.join('Spades')
                    else:
                        print('Please enter a valid letter next time. Options are c for clubs, d for diamonds, '
                            'h for hearts and s for spades')
                elif does_user_call[0].lower() == 'n':
                    was_suit_declared = False
                    caller = None
                    pass
                else:
                    print('PLease enter a valid option. y or n')
                return suit, was_suit_declared, caller
            except ValueError:
                print('Please enter a valid option')   

    def must_call_suit(self, suit: str, flipped_c: Card):
    # This forces the user to call clincher for that round. This function only runs when all players refuse to order up
    # the flipped card, and all computer player refuse to call clincher suit on the next round.
    # This only happens when the user is dealer. Rule is called 'Stick to Dealer' & forces dealer to call clincher

        was_suit_declared = False
        print('\n')
        for c in self.hand:
            print(c.display)
        while True:
            try:
                called_suit = input(
                    f'''\nYour hand is above and you can call any suit except {flipped_c.get_suit()}.\nYou must call suit. 
                    Please enter the first letter of the suit to call (c/d/h/s): ''')
                if called_suit[0].lower() == flipped_c.get_suit()[0].lower():
                    print('You entered the suit that was turned down...Please enter a different suit')
                    raise ValueError
                else:
                    if called_suit.lower() == 'c':
                        suit = suit.join('Clubs')
                        was_suit_declared = True
                    elif called_suit.lower() == 'd':
                        suit = suit.join('Diamonds')
                        was_suit_declared = True
                    elif called_suit.lower() == 'h':
                        suit = suit.join('Hearts')
                        was_suit_declared = True
                    elif called_suit.lower() == 's':
                        suit = suit.join('Spades')
                        was_suit_declared = True
                    else:
                        raise ValueError
                caller = self
                return suit, was_suit_declared, caller
            except ValueError:
                print('Please enter a valid suit')   

    def drop_card(self, flipped_c: Card, caller: Player):
    # Player adds the card to their hand, then chooses one to discard

        self.hand.append(flipped_c)
        num_cards = len(self.hand)

        while True:
            try:
                print('\nYour hand is:\n')
                for c in self.hand:
                    print(c.display)
                if caller is self:
                    card_index_to_drop = int(input(
                        f'Please enter the position 1-{num_cards} of the card to discard: ')) - 1
                else:
                    card_index_to_drop = int(input(
                        f'\n{caller.name} has ordered you to pick up the {flipped_c.display}.\n\n'
                        f'Please enter the position 1-{num_cards} of the card to discard: ')) - 1
                if card_index_to_drop in list(range(num_cards)):
                    self.hand.pop(card_index_to_drop)
                    return self
                else:
                    raise ValueError
            except ValueError:
                print(f'\nInvalid Input. Please enter a number between 1-{num_cards}\n')
    

    def lead_card(self):
        # This allows the user to play any card as the first card of the trick

        num_cards_in_hand = len(self.hand)
        print('\nYour hand is: ')
        for c in self.hand:
            print(c.display)
        while True:
            try:
                card_index_to_play = int(
                    input(f'\nPlease enter the position (1-{num_cards_in_hand}) of the card you would like to lead: ')) - 1
                lead = self.hand[card_index_to_play]
            except (ValueError, IndexError):
                print(f'\nSorry, that is not a valid number. Please enter a number: 1-{num_cards_in_hand} to choose.')
            else:
                break

        self.hand.pop(card_index_to_play)
        return lead   

    def follow_suit(self, lead_c: Card, played: list[Card]):
    # This allows the user to follow suit of the first card played
    # User must follow suit, per rules of Euchre
    # If user cannot follow suit, ValueError is raised, and user is allowed to choose any card
        print('\nThe cards played so far are: ')
        for pc in played:
            time.sleep(.4)
            print(f'{pc.display} (P{pc.owner})')
        time.sleep(1)
        print('\nYour hand is: \n')
        for c in self.hand:
            print(c.display)

        legal_cards = []
        if lead_c.left_bower_suit == 'Clubs':
            for c in self.hand:
                if c.left_bower_suit == 'Clubs':
                    legal_cards.append(c)
                else:
                    pass
        if lead_c.left_bower_suit == 'Diamonds':
            for c in self.hand:
                if c.left_bower_suit == 'Diamonds':
                    legal_cards.append(c)
                else:
                    pass
        if lead_c.left_bower_suit == 'Hearts':
            for c in self.hand:
                if c.left_bower_suit == 'Hearts':
                    legal_cards.append(c)
                else:
                    pass
        if lead_c.left_bower_suit == 'Spades':
            for c in self.hand:
                if c.left_bower_suit == 'Spades':
                    legal_cards.append(c)
                else:
                    pass

        if len(legal_cards) == 0:
            raise ValueError

        print('\nThe card(s) you can play to follow suit are: \n')
        for l in legal_cards:
            print(l.display)
        while True:
            try:
                legal_card_play_index = int(input('\nPlease enter the position of the card you\'d like to play: ')) - 1
                card_to_play = legal_cards[legal_card_play_index]
            except (ValueError, IndexError):
                print(f'Please enter a valid number between 1-{len(legal_cards)} to follow suit with that card')
            else:
                break
        self.hand.pop(self.hand.index(card_to_play))
        return card_to_play

    def choose_card(self):
    # This allows user to play any card in their hand
        while True:
            try:
                card_play_index = int(input('\nPlease enter the position of the card to play: ')) - 1
                card_to_play = self.hand[card_play_index]
                self.hand.pop(self.hand.index(card_to_play))
                return card_to_play
            except (ValueError, IndexError):
                print('Invalid input. Please enter the card position: ')

    def play_clincher(self, played: list[Card], caller: Player):
        return self.choose_card()

    def discard_bad_card(self, suit: str):
        return self.choose_card()   
    
