import random
import time
from termcolor import colored
from cards import Deck
from computer import Computer
from player import Player
from user import User


# This is the card game Euchre. Rules: https://bicyclecards.com/how-to-play/euchre/
# Cards used are 9 up to Ace. 'Going alone' for a round is not a feature of this script
# Human player is player 1. Player 3 is your teammate

class Team:
    # Teams are made up of 2 players. In real Euchre, teammates sit across the table from each other. So odd players
    # make up team1, and even numbered players make up team2
    # The human user is on team1 with Player3
    def __init__(self, player_a, player_b, points, tricks):
        self.player_a = player_a
        self.player_b = player_b
        self.points = points
        self.tricks = tricks


def assign_left_bower(best, hand):
    # This will assign the 'Correct' suit to the odd jack. it always acts as the other suit of the same color
    # Other names for odd jack: left bower

    for c in hand:
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
        else:
            pass
    return hand


def assign_points(hand, best, lead):
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
        for crd in hand:
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
        for crd in hand:
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
        for crd in hand:
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
        for crd in hand:
            crd.point = s_clincher.get(crd.card_string, 0)
    return hand


def assign_clincher(best, hand):
    for c in hand:
        if c.get_suit() == best or c.is_left_bower():
            c.clincher = True
        else:
            pass
    return hand

def determine_winning_trick_so_far(played):
    # This function determines which played is currently winning the trick, as in who has played the best card so far
    # Used to help the computer make strategic decisions about which card to play

    points_scored = {}
    for pc in played:
        points_scored[pc.owner] = pc.point
    player_in_lead = max(points_scored, key=points_scored.get)
    return player_in_lead


def assign_point_trick_winner(winning_play, play1, play2, play3, play4):
    #  Keeps track of the numbers of tricks each player has won
    if winning_play == 1:
        play1.tricks_won += 1
    elif winning_play == 2:
        play2.tricks_won += 1
    elif winning_play == 3:
        play3.tricks_won += 1
    elif winning_play == 4:
        play4.tricks_won += 1
    return play1, play2, play3, play4


def determine_trick_winner(played, testing):
    # After all 4 cards are played, this function finds the one with the highest point value. that card wins the trick
    # and the winning player (owner of that card) is returned
    cards_points = {}
    for c in played:
        cards_points[c] = c.point
        if not testing:
            print(f'{c.display} (P{c.owner})')
            time.sleep(.4)
    winning_card = max(cards_points, key=cards_points.get)
    winner = winning_card.owner
    not testing and print(f'\nPlayer{winner} won with the {winning_card.display}')
    return winner


def play_trick(p1, p2, p3, p4, round_leader, best_suit, caller, testing):
    # The user can now play a card by choosing the index (1-5) of the card to play. That suit is lead
    # and must be followed by other players
    not testing and print(colored(f'\nClincher: {best_suit} ({caller.name})', 'green'))

    p1.hand = assign_clincher(best_suit, p1.hand)
    p2.hand = assign_clincher(best_suit, p2.hand)
    p3.hand = assign_clincher(best_suit, p3.hand)
    p4.hand = assign_clincher(best_suit, p4.hand)

    player_map = {1: p1, 2: p2, 3: p3, 4: p4}
    round_order = [round_leader, round_leader % 4 + 1, (round_leader + 1) % 4 + 1, (round_leader + 2) % 4 + 1]

    lead_card = player_map[round_leader].lead_card()

    played_cards = [lead_card]

    p1.hand = assign_points(p1.hand, best_suit, lead_card)
    p2.hand = assign_points(p2.hand, best_suit, lead_card)
    p3.hand = assign_points(p3.hand, best_suit, lead_card)
    p4.hand = assign_points(p4.hand, best_suit, lead_card)

    player_in_lead = round_leader

    not testing and time.sleep(1.75)

    for player in round_order[1:]:
        try:
            played_card = player_map[player].follow_suit(lead_card, played_cards)
        except ValueError:
            try:
                if player_in_lead == (player + 1) % 4 + 1:
                    raise ValueError
                else:
                    played_card = player_map[player].play_clincher(played_cards, caller)
            except ValueError:
                played_card = player_map[player].discard_bad_card(best_suit)
        played_cards.append(played_card)
        player_in_lead = determine_winning_trick_so_far(played_cards)

    winning_player = determine_trick_winner(played_cards, testing)

    p1, p2, p3, p4 = assign_point_trick_winner(winning_player, p1, p2, p3, p4)

    not testing and print(colored(f'\nRound Score: {p1.tricks_won + p3.tricks_won}-{p2.tricks_won + p4.tricks_won}', 'green'))

    return p1, p2, p3, p4, winning_player


def play_round(team1, team2, player1, player2, player3, player4, deck, dlr_index, dlr, ldr_index, testing):
    #  This function runs each round of Euchre and will be looped over until enough points are scored (11 by 1 team)
    not testing and deck.show()
    deck.deal_cards(player1)
    deck.deal_cards(player2)
    deck.deal_cards(player3)
    deck.deal_cards(player4)

    player1.tricks_won = 0
    player2.tricks_won = 0
    player3.tricks_won = 0
    player4.tricks_won = 0

    flipped_card = deck.flip_card()

    not testing and print(f'\nDealer: {dlr.name}\nFlipped: {flipped_card.display}\n')
    not testing and time.sleep(1.5)

    best_suit = ''

    player1.evaluate_cards()
    player2.evaluate_cards()
    player3.evaluate_cards()
    player4.evaluate_cards()

    player_map = {1: player1, 2: player2, 3: player3, 4: player4}

    player_order = [(dlr_index) % 4 + 1, (dlr_index + 1) % 4 + 1, (dlr_index + 2) % 4 + 1, dlr_index]

    was_suit_picked = False

    for player in player_order:
        player_map[player], best_suit, was_suit_picked, player_map[dlr_index], calling_player = \
            player_map[player].order_up_card(best_suit, flipped_card, player_map[dlr_index], testing)
        if was_suit_picked:
            break

    if not was_suit_picked:
        for player in player_order:
            best_suit, was_suit_picked, calling_player = \
                player_map[player].choose_call_suit(best_suit, flipped_card, testing)
            if was_suit_picked:
                break

    if not was_suit_picked:
        best_suit, was_suit_picked, calling_player = player_map[dlr_index].must_call_suit(best_suit, flipped_card)

    for c in player1.hand:
        c.owner = 1
    for c in player2.hand:
        c.owner = 2
    for c in player3.hand:
        c.owner = 3
    for c in player4.hand:
        c.owner = 4

    not testing and print(colored(f'{calling_player.name}: {best_suit} is clincher suit.', 'green'))
    not testing and time.sleep(1.3)

    player1.hand = assign_left_bower(best_suit, player1.hand)
    player2.hand = assign_left_bower(best_suit, player2.hand)
    player3.hand = assign_left_bower(best_suit, player3.hand)
    player4.hand = assign_left_bower(best_suit, player4.hand)

    for _ in range(5):
        player1, player2, player3, player4, ldr_index = play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player, testing)

    team1.tricks = player1.tricks_won + player3.tricks_won
    team2.tricks = player2.tricks_won + player4.tricks_won

    if team1.tricks > team2.tricks:
        if calling_player.name == 'Player2' or calling_player.name == 'Player4' or team1.tricks == 5:
            team1.points += 2
            not testing and print(f'\nYou win! Team 1 won, taking {team1.tricks} tricks. Your team scored 2 points!')
        else:
            team1.points += 1
            not testing and print(f'\nYou win! Team 1 won, taking {team1.tricks} tricks. Your team scored 1 point!')
    elif team2.tricks > team1.tricks:
        if calling_player.name == 'Player1' or calling_player.name == 'Player3' or team2.tricks == 5:
            team2.points += 2
            not testing and print(f'\nYou lost this round! Team 2 won, taking {team2.tricks} tricks. They scored 2 points!')
        else:
            team2.points += 1
            not testing and print(f'\nYou lost this round! Team 2 won, taking {team2.tricks} tricks. They scored 1 point!')

    not testing and time.sleep(2.5)
    not testing and print(f'\nThe game score is {team1.points}-{team2.points}')
    not testing and time.sleep(2.5)

    return team1, team2, player1, player2, player3, player4

def play_game(p1, p2, p3, p4, testing):
    # Create the 4 players and the deck out of the 24 possible cards.
    # Randomly assign 5 cards to each player (no repeats)
    # Flip one remaining card

    d = Deck()
    d.show()

    team_1 = Team(p1, p3, 0, 0)
    team_2 = Team(p2, p4, 0, 0)


    players = {p1: 1, p2: 2, p3: 3, p4: 4}
    dealer, dealer_index = random.choice(list(players.items()))
    leader_index = (dealer_index % 4) + 1

    while team_1.points < 11 and team_2.points < 11:
        team_1, team_2, p1, p2, p3, p4 = play_round(team_1, team_2, p1, p2, p3,
                                                                            p4, d, dealer_index, dealer, leader_index, testing)
        dealer_index = dealer_index % 4 + 1
        leader_index = leader_index % 4 + 1
        dealer = list(players.keys())[list(players.values()).index(dealer_index)]
        d.destroy()
        d.build()
        if team_1.points >= 11:
            not testing and print(f'You win the game! Final Score: {team_1.points}-{team_2.points}')
            return "Team 1"
        elif team_2.points >= 11:
            not testing and print(f'You lose the game! Final Score: {team_1.points}-{team_2.points}')
            return "Team 2"


def main():
    # prompt user for testing or not
    val = input("Enter \"t\" if you would like to test the AI. ")
    testing = True if val == "t" else False

    if testing:
        wins = {"Team 1": 0, "Team 2": 0}
        for _ in range(0, 10000):
            winning_team = play_game(Computer(1), Computer(2), Computer(3), Computer(4), testing=True)
            wins[winning_team] += 1
        print(wins)
    else:
        play_game(User(1), Computer(2), Computer(3), Computer(4), testing=False)

if __name__ == "__main__":
    main()