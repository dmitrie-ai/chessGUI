from chess_board import *
from player import PlayerHuman, PlayerAI, PlayerStockfish
from game import HumanVsHumanGame, HumanVsAI, AIvsAI, menu

pygame.init()  # initialise pygame
GAME_DISPLAY = pygame.display.set_mode((850, 600))  # set the pygame.display object
pygame.display.set_caption("CHESS v4.2.0")  # set the title of the window
CLOCK = pygame.time.Clock()


def __main__():
    menu(GAME_DISPLAY)


def test():
    board = Board(GAME_DISPLAY)
    AI_player = PlayerAI("W", board, 1, False)
    AI_player2 = PlayerAI("B", board, 3, True)
    SF_player1 = PlayerStockfish("B", board, 9, True)
    SF_player2 = PlayerStockfish("W", board, 10, False)

    AIvsAIgame = AIvsAI(playerB=SF_player1, playerW=SF_player2, board=board, game_display=GAME_DISPLAY)
    AIvsAIgame.start()


# test()


__main__()
