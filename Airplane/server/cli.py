from game import Game, Action


def main():
    game = Game()
    while not game.game_over and not game.draw_flag:
        print(game.draw())
        inp = input()
        if inp == 'a':
            action = Action.MOVE_LEFT
        elif inp == 'd':
            action = Action.MOVE_RIGHT
        else:
            action = None
        game.tick(action)


if __name__ == '__main__':
    main()
