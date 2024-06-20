import pygame
from game import Game


def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    pygame.display.set_mode((screen_width, screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Stack Attack")

    game = Game(screen_width, screen_height)
    game.run()


if __name__ == "__main__":
    main()