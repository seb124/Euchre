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
    # This is called at the start of every round after the 1st card is played
    # This gives point values to every card that could potentially win the round (clincher > suit of 1st card)
    # This will act as a ranking system to determine which was the best card played that round

        c_clincher = {'Jack of Clubs': 13, 'Jack of Spades': 12, 'Ace of Clubs': 11, 'King of Clubs': 10,
                    'Queen of Clubs': 9, '10 of Clubs': 8, '9 of Clubs': 7}
        d_clincher = {'Jack of Diamonds': 13, 'Jack of Hearts': 12, 'Ace of Diamonds': 11, 'King of Diamonds': 10,
                    'Queen of Diamonds': 9, '10 of Diamonds': 8, '9 of Diamonds': 7}
        h_clincher = {'Jack of Hearts': 13, 'Jack of Diamonds': 12, 'Ace of Hearts': 11, 'King of Hearts': 10,
                    'Queen of Hearts': 9, '10 of Hearts': 8, '9 of Hearts': 7}
        s_clincher = {'Jack of Spades': 13, 'Jack of Clubs': 12, 'Ace of Spades': 11, 'King of Spades': 10,
                    'Queen of Spades': 9, '10 of Spades': 8, '9 of Spades': 7}
        c_lead = {'Ace of Clubs': 6, 'King of Clubs': 5, 'Queen of Clubs': 4, 'Jack of Clubs': 3,
                '10 of Clubs': 2, '9 of Clubs': 1}
        d_lead = {'Ace of Diamonds': 6, 'King of Diamonds': 5, 'Queen of Diamonds': 4, 'Jack of Diamonds': 3,
                '10 of Diamonds': 2, '9 of Diamonds': 1}
        h_lead = {'Ace of Hearts': 6, 'King of Hearts': 5, 'Queen of Hearts': 4, 'Jack of Hearts': 3,
                '10 of Hearts': 2, '9 of Hearts': 1}
        s_lead = {'Ace of Spades': 6, 'King of Spades': 5, 'Queen of Spades': 4, 'Jack of Spades': 3,
                '10 of Spades': 2, '9 of Spades': 1}

        if best == 'Clubs':
            if lead.left_bower_suit == 'Spades':
                s_lead.pop('Jack of Spades')
                c_clincher.update(s_lead)
            elif lead.left_bower_suit == 'Hearts':
                c_clincher.update(h_lead)
            elif lead.left_bower_suit == 'Diamonds':
                c_clincher.update(d_lead)
            elif lead.left_bower_suit == 'Clubs':
                pass
            lead.point = c_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = c_clincher.get(crd.card_string, 0)

        elif best == 'Diamonds':
            if lead.left_bower_suit == 'Clubs':
                d_clincher.update(c_lead)
            elif lead.left_bower_suit == 'Diamonds':
                pass
            elif lead.left_bower_suit == 'Hearts':
                h_lead.pop('Jack of Hearts')
                d_clincher.update(h_lead)
            elif lead.left_bower_suit == 'Spades':
                d_clincher.update(s_lead)
            lead.point = d_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = d_clincher.get(crd.card_string, 0)

        elif best == 'Hearts':
            if lead.left_bower_suit == 'Clubs':
                h_clincher.update(c_lead)
            elif lead.left_bower_suit == 'Diamonds':
                d_lead.pop('Jack of Diamonds')
                h_clincher.update(d_lead)
            elif lead.left_bower_suit == 'Hearts':
                pass
            elif lead.left_bower_suit == 'Spades':
                h_clincher.update(s_lead)
            lead.point = h_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = h_clincher.get(crd.card_string, 0)

        elif best == 'Spades':
            if lead.left_bower_suit == 'Clubs':
                c_lead.pop('Jack of Clubs')
                s_clincher.update(c_lead)
            elif lead.left_bower_suit == 'Diamonds':
                s_clincher.update(d_lead)
            elif lead.left_bower_suit == 'Hearts':
                s_clincher.update(h_lead)
            elif lead.left_bower_suit == 'Spades':
                pass
            lead.point = s_clincher.get(lead.card_string, 0)
            for crd in self.hand:
                crd.point = s_clincher.get(crd.card_string, 0)

    def evaluate_cards(self):
    # This function is run before clincher suit is called
    # It assigns points based on the cards in the players hand
    # It gives points to each suit based on how strong the players hand would be if that suit were clincher
    # This exists so the computer players can use strategy to decide whether to call clincher and which suit to call

        self.card_values = [0, 0, 0, 0]  # [Clubs, Diamonds, Hearts, Spades]
        point_dict_clubs = {'Jack of Clubs': 15, 'Jack of Spades': 13, 'Ace of Clubs': 11, 'King of Clubs': 10,
                            'Queen of Clubs': 9, '10 of Clubs': 8, '9 of Clubs': 7,
                            'Ace of Diamonds': 4, 'Ace of Hearts': 4, 'Ace of Spades': 4}
        point_dict_diamonds = {'Jack of Diamonds': 15, 'Jack of Hearts': 13, 'Ace of Diamonds': 11,
                               'King of Diamonds': 10, 'Queen of Diamonds': 9, '10 of Diamonds': 8, '9 of Diamonds': 7,
                               'Ace of Clubs': 4, 'Ace of Hearts': 4, 'Ace of Spades': 4}
        point_dict_hearts = {'Jack of Hearts': 15, 'Jack of Diamonds': 13, 'Ace of Hearts': 11, 'King of Hearts': 10,
                             'Queen of Hearts': 9, '10 of Hearts': 8, '9 of Hearts': 7,
                             'Ace of Clubs': 4, 'Ace of Diamonds': 4, 'Ace of Spades': 4}
        point_dict_spades = {'Jack of Spades': 15, 'Jack of Clubs': 13, 'Ace of Spades': 11, 'King of Spades': 10,
                             'Queen of Spades': 9, '10 of Spades': 8, '9 of Spades': 7,
                             'Ace of Clubs': 4, 'Ace of Diamonds': 4, 'Ace of Hearts': 4}
        for c in self.hand:
            if c.card_string in point_dict_clubs:
                self.card_values[0] += point_dict_clubs.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_diamonds:
                self.card_values[1] += point_dict_diamonds.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_hearts:
                self.card_values[2] += point_dict_hearts.get(c.card_string)
            else:
                pass
            if c.card_string in point_dict_spades:
                self.card_values[3] += point_dict_spades.get(c.card_string)
        return self.card_values   

    def order_up_card(self, suit: str, flipped_c: Card, dlr_index: int, dealer):
        pass

    def choose_call_suit(self, suit: str, flipped_c: Card, testing: bool, dlr_index: int):
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

    def update_probability_table(self, player_num: int, action: str, flipped_c: Card, trump_suit: str):
        pass

    def reset_probability_table(self, deck: Deck):
        pass

    def generate_smack_talk(self, action: str):
        pass

class Team:
    # Teams are made up of 2 players. In real Euchre, teammates sit across the table from each other. So odd players
    # make up team1, and even numbered players make up team2
    def __init__(self, player_a, player_b, points, tricks):
        self.player_a = player_a
        self.player_b = player_b
        self.points = points
        self.tricks = tricks