from argparse import ArgumentParser

from application import Application
from model import TagModel


def main(width: int, height: int):
    game = TagModel(width, height)
    game.shuffle()
    app = Application(None, game)
    app.mainloop()


if __name__ == '__main__':
    parser = ArgumentParser("Tag game")
    parser.add_argument('-fw', dest='width', type=int, default=4, help="Game field width")
    parser.add_argument('-fh', dest='height', type=int, default=4, help="Game field height")

    args = parser.parse_args()

    main(args.width, args.height)
