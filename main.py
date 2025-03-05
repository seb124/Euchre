import engine
from classes.computer import Computer
from classes.user import User

# TODO: make main function that can read JSON file (config.json) and call play_game with those args - makes it really easy to test


def main():
    # prompt user for testing or not
    val = input("Enter \"t\" if you would like to test the AI. ")
    testing = True if val == "t" else False

    if testing:
        wins = {"Team 1": 0, "Team 2": 0}
        for _ in range(0, 1000):
            winning_team = engine.play_game(Computer(1), Computer(2), Computer(3), Computer(4), testing=True)
            wins[winning_team] += 1
        print(wins)
    else:
        engine.play_game(User(1), Computer(2), Computer(3), Computer(4), testing=False)

if __name__ == "__main__":
    main()