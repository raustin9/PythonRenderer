import argparse
import subprocess


def run_game():
    subprocess.run(["py", "src/game.py"])
    print("running game...")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('game', help="Run the game")
    args = parser.parse_args()

    if args.game:
        run_game()