import argparse
import subprocess


def run_game():
    subprocess.run(["py", "src/game.py"])
    print("running game...")

def test_game():
    subprocess.run(["scalene", "src/game.py"])
    print("profiling game...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', help="Run the game", required=False, default="")
    parser.add_argument('--profile', help="Profile the game using Scalene", required=False, default="")
    args = parser.parse_args()

    if args.game:
        run_game()
    elif args.profile:
        test_game()