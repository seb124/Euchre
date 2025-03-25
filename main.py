import engine
from classes.computer import Computer
from classes.aiv1 import AIV1
from classes.aiv2 import AIV2
from classes.aiv3 import AIV3
from classes.aiv4 import AIV4
from classes.user import User
import json

player_mapper = {"User": User, "Computer": Computer, "AIV1": AIV1, "AIV2": AIV2, "AIV3": AIV3, "AIV4": AIV4}

def main():
    # prompt user for testing or not
    testing = True

    with open('config/config.json') as f:
            config = json.load(f) 

    player_1 = player_mapper[config["player-1"]]
    player_2 = player_mapper[config["player-2"]]
    player_3 = player_mapper[config["player-3"]]
    player_4 = player_mapper[config["player-4"]]

    if player_1 is User or player_2 is User or player_3 is User or player_4 is User:
        testing = False

    if testing:
        wins = {"Team 1": 0, "Team 2": 0}
        for _ in range(0, config["number-iterations"]):
            winning_team = engine.play_game(player_1(1), player_2(2), player_3(3), player_4(4), testing=True)
            wins[winning_team] += 1
        print(wins)
    else:
        engine.play_game(player_1(1), player_2(2), player_3(3), player_4(4), testing=False)

if __name__ == "__main__":
    main()