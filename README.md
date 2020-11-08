# chessGUI
Chess GUI allowing local 1v1 against another human or against various levels of AI(stockfish).
For the levels 1-4, it uses my own Minimax with alpha beta pruning with respective depths. At levels higher than 4, it uses the stockfish chess engine with depth(level-4) to make the sofware more accessible since stockfish level 1 is still quite challenging for absolute begginners

Features:
* Undo move
* Suggested move from level 16(max is 20 but is adjusted for speed. can be changed in game.py) stockfish at any point in the game
* player vs player local game
* player vs AI local game    20 levels of difficulty

Dependencies:
* pygame
