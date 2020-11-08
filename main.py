from chess_board import *
from player import PlayerHuman, PlayerAI, PlayerStockfish
from game import HumanVsHumanGame, HumanVsAI, AIvsAI, menu

pygame.init()  # initialise pygame
GAME_DISPLAY = pygame.display.set_mode((850, 600))  # set the pygame.display object
pygame.display.set_caption("CHESS v4.2.0")  # set the title of the window
CLOCK = pygame.time.Clock()


def __main__():
    menu(GAME_DISPLAY)

__main__()
