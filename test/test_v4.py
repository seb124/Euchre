import sys
import os
import scipy.stats
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from classes.aiv3 import AIV3
from classes.aiv4 import AIV4
from classes.cards import Deck
from classes.player import Team
import engine

# This test examines how well AIV4 actually performs, since its updated functions are not always called.
# Every 100 games, a new "point" will be added to the list

x = [] # % of rounds in 100 games that go to a second "pass" (and thus the updated AIV4 functions are called)
y = [] # % of those rounds that a team of AIV4s wins (against a team of AIV3s)

# create global variables (*for testing purposes only*)
second_pass_count = 0
round_wins = 0
round_count = 0

def play_round(team1, team2, player1, player2, player3, player4, deck, dlr_index, dlr, ldr_index, testing):
    deck.deal_cards(player1)
    deck.deal_cards(player2)
    deck.deal_cards(player3)
    deck.deal_cards(player4)

    player1.tricks_won = 0
    player2.tricks_won = 0
    player3.tricks_won = 0
    player4.tricks_won = 0

    flipped_card = deck.flip_card()



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
            player_map[player].order_up_card(best_suit, flipped_card, dlr_index, player_map[dlr_index], testing)
        if was_suit_picked:
            break
        else:
            other_players = [player_num for player_num in player_order if player_num != player]
            for other_player in other_players:
                player_map[other_player].update_probability_table(player, "pass", flipped_card.suit)

    if not was_suit_picked:
        global second_pass_count
        second_pass_count += 1
        for player in player_order:
            best_suit, was_suit_picked, calling_player = \
                player_map[player].choose_call_suit(best_suit, flipped_card, testing, dlr_index)
            if was_suit_picked:
                break
            else:
                other_players = [player_num for player_num in player_order if player_num != player]
                for other_player in other_players:
                    for suit in ['Clubs', 'Diamonds', 'Hearts', 'Spades']:
                        if suit != flipped_card.suit:
                            player_map[other_player].update_probability_table(player, "pass", suit)


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

    player1.assign_left_bower(best_suit)
    player2.assign_left_bower(best_suit)
    player3.assign_left_bower(best_suit)
    player4.assign_left_bower(best_suit)


    for _ in range(5):
        player1, player2, player3, player4, ldr_index = engine.play_trick(player1, player2, player3, player4,
                                                               ldr_index, best_suit, calling_player, testing)

    team1.tricks = player1.tricks_won + player3.tricks_won
    team2.tricks = player2.tricks_won + player4.tricks_won

    if team1.tricks > team2.tricks:
        global round_wins
        round_wins += 1
        if calling_player.name == 'Player2' or calling_player.name == 'Player4' or team1.tricks == 5:
            team1.points += 2
        else:
            team1.points += 1
    elif team2.tricks > team1.tricks:
        if calling_player.name == 'Player1' or calling_player.name == 'Player3' or team2.tricks == 5:
            team2.points += 2
        else:
            team2.points += 1


    return team1, team2, player1, player2, player3, player4

def play_game(p1, p2, p3, p4, testing):

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
        global round_count
        round_count += 1
        dealer_index = dealer_index % 4 + 1
        leader_index = leader_index % 4 + 1
        dealer = list(players.keys())[list(players.values()).index(dealer_index)]
        d.destroy()
        d.build()

        p1.reset_probability_table(d)
        p2.reset_probability_table(d)
        p3.reset_probability_table(d)
        p4.reset_probability_table(d)

        if team_1.points >= 11:
            return "Team 1"
        elif team_2.points >= 11:
            return "Team 2"

def data_collection():
    # run this by uncommenting function below if you want to collect more data in the v4_datapoints.txt file

    for i in range(1000000):
        play_game(AIV4(1), AIV3(2), AIV4(3), AIV3(4), True)

        if i != 0 and i % 100 == 0:
            global second_pass_count
            global round_count
            global round_wins

            x.append(second_pass_count / round_count)
            y.append(round_wins / round_count)

            file = open("test/data/v4_datapoints.txt", "a")
            file.write(f"{(second_pass_count / round_count)} {round_wins / round_count}\n")

            round_wins = 0
            second_pass_count = 0
            round_count = 0


# data_collection()


def statistical_analysis():
    # run to compute r-value and p-value, among other things
    # hypothesize that the slope of the line (proportional to correlation coefficient) is nonzero, hope that it's positive
    x = []
    y = []
    with open("test/data/v4_datapoints.txt") as pts:
        for line in pts:
            arr = line.split(" ")
            x.append(float(arr[0]))
            y.append(float(arr[1]))
    
    result = scipy.stats.linregress(x, y)

    # With one iteration of 1 million games of Euchre, the results (with data found in v4_datapoints.txt) are:
    print(result.rvalue) # prints 0.0.03945200921644532
    print(result.pvalue) # prints 7.938671586906828e-05 (< 0.05)

    # So, we fail to reject that the slope is 0 and conclude that there is a slight positive correlation between the number of rounds
    # that call AIV4's new function and the number of those rounds that a team of AIV4s wins. So, AIV4 does slightly improve performance.


statistical_analysis()