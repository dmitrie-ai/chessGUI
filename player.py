import random
from stockfish_parser import *
from miscellaneous import algebraic_to_array_form
import time


class Player:
    '''
    Static Parent class
    '''

    def __init__(self, color, board, is_opposite):
        '''
        :param color: CHAR. "W"|"B"
        :param board: Board class
        :param is_opposite: BOOL. Whether the player is on the opposite or class side of the board
        '''
        self.is_human = None
        self._board = board
        self.is_opposite = is_opposite
        self.color = color
        if self.color == "W":
            self.is_turn = True
        else:
            self.is_turn = False
        self.captured_pieces = []
        # automatically gets the king position depending on is_opposite and color
        if self.is_opposite:
            if self.color == "W":
                self.king_pos = (0, 3)
                self.k_rook_pos = (0, 0)
                self.q_rook_pos = (0, 7)
            else:
                self.king_pos = (0, 4)
                self.k_rook_pos = (0, 7)
                self.q_rook_pos = (0, 0)
        else:
            if self.color == "W":
                self.king_pos = (7, 4)
                self.k_rook_pos = (7, 7)
                self.q_rook_pos = (7, 0)
            else:
                self.king_pos = (7, 3)
                self.k_rook_pos = (7, 0)
                self.q_rook_pos = (7, 7)

    def get_color(self):
        return self.color

    def set_board(self, new_board):
        self._board = new_board

    def get_board(self):
        return self._board

    def is_in_check(self):
        return self._board.is_under_attack(self.color, [self.king_pos])

    def is_in_checkmate(self):
        legal_moves = self._board.get_legal_moves(self)
        # if the player has no legal moves and is already in check
        if len(legal_moves) == 0 and self.is_in_check():
            return True
        return False

    def is_stalemate(self):
        # if the player isn't in check but has no legal moves
        if self.is_in_check() == False:
            if len(self._board.get_legal_moves(self)) == 0:
                return True
            else:
                return False
        else:
            return False

    def get_captured_pieces(self):
        return self.captured_pieces

    def move_piece(self, piece, new_square):
        '''
        moving a piece to a particular square
        :param piece: Piece object
        :param new_square: TUPLE of INTEGERS. (row,col)
        '''
        self._board.push_move(
            f'{piece.get_pos()[0]}{piece.get_pos()[1]},{new_square[0]}{new_square[1]}')
        piece.is_first_move = False
        self.deselect_piece(piece)

    def select_piece(self, piece):
        '''
        act of clicking on a friendly piece
        :param piece: Piece object
        '''
        piece.select()
        self._board.moves_displayed = True
        self._board.set_selected_piece(piece)
        valid_moves = piece.get_valid_moves()
        self._board.draw_green_squares(valid_moves)

    def deselect_piece(self, piece):
        '''
        Act of deselecting by clicking again on the same piece or  clicking on a different piece whilst another is
        selected
        :param piece: Piece object
        '''
        piece.deselect()
        self._board.moves_displayed = False
        self._board.draw_board()

    def castle(self, side):
        '''
        Act of castling
        :param side: CHAR. which side to castle i.e. "Q" or "K"
        '''
        if self.is_opposite:
            left_rook = self._board.get_piece(0, 0)
            right_rook = self._board.get_piece(0, 7)
            if side == "Q":
                if self.color == "W":
                    king_piece = self._board.get_piece(0, 3)
                    self.move_piece(king_piece, (0, 5))
                    self.move_piece(right_rook, (0, 4))

                else:
                    king_piece = self._board.get_piece(0, 4)
                    self.move_piece(king_piece, (0, 2))
                    self.move_piece(left_rook, (0, 3))
            elif side == "K":
                if self.color == "W":
                    king_piece = self._board.get_piece(0, 3)
                    self.move_piece(king_piece, (0, 1))
                    self.move_piece(left_rook, (0, 2))
                else:
                    king_piece = self._board.get_piece(0, 4)
                    self.move_piece(king_piece, (0, 6))
                    self.move_piece(right_rook, (0, 5))
        else:
            left_rook = self._board.get_piece(7, 0)
            right_rook = self._board.get_piece(7, 7)
            if side == "Q":
                if self.color == "W":
                    king_piece = self._board.get_piece(7, 4)
                    self.move_piece(king_piece, (7, 2))
                    self.move_piece(left_rook, (7, 3))
                else:
                    king_piece = self._board.get_piece(7, 3)
                    self.move_piece(king_piece, (7, 5))
                    self.move_piece(right_rook, (7, 4))
            elif side == "K":
                if self.color == "W":
                    king_piece = self._board.get_piece(7, 4)
                    self.move_piece(king_piece, (7, 6))
                    self.move_piece(right_rook, (7, 5))
                else:
                    king_piece = self._board.get_piece(7, 3)
                    self.move_piece(king_piece, (7, 1))
                    self.move_piece(left_rook, (7, 2))


class PlayerHuman(Player):
    def __init__(self, color, board, is_opposite):
        super().__init__(color, board, is_opposite)
        self.is_human = True


class PlayerStockfish(Player):
    '''
    AI player that uses teh Stockfish engine to calculate moves
    '''

    def __init__(self, color, board, depth, is_opposite=True):
        super().__init__(color, board, is_opposite)
        self.is_human = False
        self.depth = depth
        self.is_stockfish = True  # identify as stockfish player
        # allows to communicate with Stockfish engine executable
        self.handler = init_stockfish(self.depth)

    def set_depth(self, value):
        '''
        set depth
        :param value: INTEGER
        '''
        self.depth = value
        del self.handler  # del the Stockfish object
        self.handler = init_stockfish(self.depth)  # Create another Stockfish object with updated depth

    def get_best_move(self, fen):
        '''
        :param fen: STRING. fen string of the game state
        :return:STRING. best move
        '''
        move = get_best_move(self.handler, fen)
        if move == "0-0":  # King side castling
            move = f'C,{self.king_pos[0]}{self.king_pos[1]},K'
            return move
        elif move == "0-0-0":  # queen side castling
            move = f'C,{self.king_pos[0]}{self.king_pos[1]},Q'
            return move
        else:
            # teh move is given in algebraic form. The program uses a different format(see Board)
            start_pos = algebraic_to_array_form(move[:2])
            end_pos = algebraic_to_array_form(move[2:])
            if self.is_opposite and self.color == "W":  # the best move is given assuming that white is the close player and black is the opposite player
                # reflects the move so that it works with white being opposite
                start_pos = (-start_pos[0] + 7, start_pos[1])
                end_pos = (-end_pos[0] + 7, end_pos[1])
            if move[-1] in ["n", "q", "r", "b"]:  # if promotion is involved
                return (f'{start_pos[0]}{start_pos[1]},{end_pos[0]}{end_pos[1]}',
                        f"P,{end_pos[0]}{end_pos[1]},{move[-1].upper()}")
            else:

                return f'{start_pos[0]}{start_pos[1]},{end_pos[0]}{end_pos[1]}'

    def next_move(self, fen):
        '''
        perform calcualated move
        :param fen: STRING. fen sring of game state
        '''
        best_move = self.get_best_move(fen)
        if self.depth < 10:  # So it's not as fast to make a move
            time.sleep(0)
        if len(best_move) == 2:  # if promotion is involved
            # do the move
            self._board.push_move(best_move[0])
            # do promotion
            self._board.push_move(best_move[1])
        else:  # if promotion isn't involved
            self._board.push_move(best_move)


class PlayerAI(Player):
    '''
    My AI player
    '''

    def __init__(self, color, board, depth, is_opposite=True):
        super().__init__(color, board, is_opposite)
        self.is_human = False
        self.depth = depth
        self.is_stockfish = False

    def set_depth(self, value):
        self.depth = value

    def _calculate_material_value(self, board):
        '''
        score boards for each piece type capital=white or close side   and lowercase=black or opposite side of board.
        Used in the evaluation function AI to reward and penalise good and bad positions for particular piece types.
        https://www.chessprogramming.org/Simplified_Evaluation_Function

        '''
        P_scores = [[0, 0, 0, 0, 0, 0, 0, 0, ],
                    [50, 50, 50, 50, 50, 50, 50, 50],
                    [10, 10, 20, 30, 30, 20, 10, 10],
                    [5, 5, 10, 25, 25, 10, 5, 5],
                    [0, 0, 0, 20, 20, 0, 0, 0],
                    [5, -5, -10, 0, 0, -10, -5, 5],
                    [5, 10, 10, -20, -20, 10, 10, 5],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        p_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [5, 10, 10, -20, -20, 10, 10, 5],
                    [5, -5, -10, 0, 0, -10, -5, 5],
                    [0, 0, 0, 20, 20, 0, 0, 0],
                    [5, 5, 10, 25, 25, 10, 5, 5],
                    [10, 10, 20, 30, 30, 20, 10, 10],
                    [50, 50, 50, 50, 50, 50, 50, 50],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

        N_scores = [[-50, -40, -30, -30, -30, -30, -40, -50],
                    [-40, -20, 0, 0, 0, 0, -20, -40],
                    [-30, 0, 10, 15, 15, 10, 0, -30],
                    [-30, 5, 15, 20, 20, 15, 5, -30],
                    [-30, 0, 15, 20, 20, 15, 0, -30],
                    [-30, 5, 10, 15, 15, 10, 5, -30],
                    [-40, -20, 0, 5, 5, 0, -20, -40],
                    [-50, -40, -30, -30, -30, -30, -40, -50]]

        n_scores = [[-50, -40, -30, -30, -30, -30, -40, -50],
                    [-40, -20, 0, 5, 5, 0, -20, -40],
                    [-30, 5, 10, 15, 15, 10, 5, -30],
                    [-30, 0, 15, 20, 20, 15, 0, -30],
                    [-30, 5, 15, 20, 20, 15, 5, -30],
                    [-30, 0, 10, 15, 15, 10, 0, -30],
                    [-40, -20, 0, 0, 0, 0, -20, -40],
                    [-50, -40, -30, -30, -30, -30, -40, -50]]
        B_scores = [[-20, -10, -10, -10, -10, -10, -10, -20],
                    [-10, 0, 0, 0, 0, 0, 0, -10],
                    [-10, 0, 5, 10, 10, 5, 0, -10],
                    [-10, 5, 5, 10, 10, 5, 5, -10],
                    [-10, 0, 10, 10, 10, 10, 0, -10],
                    [-10, 10, 10, 10, 10, 10, 10, -10],
                    [-10, 5, 0, 0, 0, 0, 5, -10],
                    [-20, -10, -10, -10, -10, -10, -10, -20]]

        b_scores = [[-20, -10, -10, -10, -10, -10, -10, -20],
                    [-10, 5, 0, 0, 0, 0, 5, -10],
                    [-10, 10, 10, 10, 10, 10, 10, -10],
                    [-10, 0, 10, 10, 10, 10, 0, -10],
                    [-10, 5, 5, 10, 10, 5, 5, -10],
                    [-10, 0, 5, 10, 10, 5, 0, -10],
                    [-10, 0, 0, 0, 0, 0, 0, -10],
                    [-20, -10, -10, -10, -10, -10, -10, -20]]
        R_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [5, 10, 10, 10, 10, 10, 10, 5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [0, 0, 0, 5, 5, 0, 0, 0]]
        r_scores = [[0, 0, 0, 5, 5, 0, 0, 0],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [-5, 0, 0, 0, 0, 0, 0, -5],
                    [5, 10, 10, 10, 10, 10, 10, 5],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
        Q_scores = [[-20, -10, -10, -5, -5, -10, -10, -20],
                    [-10, 0, 0, 0, 0, 0, 0, -10],
                    [-10, 0, 5, 5, 5, 5, 0, -10],
                    [-5, 0, 5, 5, 5, 5, 0, -5],
                    [0, 0, 5, 5, 5, 5, 0, -5],
                    [-10, 5, 5, 5, 5, 5, 0, -10],
                    [-10, 0, 5, 0, 0, 0, 0, -10],
                    [-20, -10, -10, -5, -5, -10, -10, -20]]
        q_scores = [[-20, -10, -10, -5, -5, -10, -10, -20],
                    [-10, 0, 5, 0, 0, 0, 0, -10],
                    [-10, 5, 5, 5, 5, 5, 0, -10],
                    [0, 0, 5, 5, 5, 5, 0, -5],
                    [-5, 0, 5, 5, 5, 5, 0, -5],
                    [-10, 0, 5, 5, 5, 5, 0, -10],
                    [-10, 0, 0, 0, 0, 0, 0, -10],
                    [-20, -10, -10, -5, -5, -10, -10, -20]]
        K_scores = [[-30, -40, -40, -50, -50, -40, -40, -30],
                    [-30, -40, -40, -50, -50, -40, -40, -30],
                    [-30, -40, -40, -50, -50, -40, -40, -30],
                    [-30, -40, -40, -50, -50, -40, -40, -30],
                    [-20, -30, -30, -40, -40, -30, -30, -20],
                    [-10, -20, -20, -20, -20, -20, -20, -10],
                    [20, 20, 0, 0, 0, 0, 20, 20],
                    [20, 30, 10, 0, 0, 10, 30, 20]]

        k_scores = [[20, 30, 10, 0, 0, 10, 30, 20],
                    [20, 20, 0, 0, 0, 0, 20, 20],
                    [-10, -20, -20, -20, -20, -20, -20, -10],
                    [-20, -30, -30, -40, -40, -30, -30, -20],
                    [-30, -40, -40, -50, -50, -40, -40, -30],
                    [-30, -40, -40, -50, -50, -40, -40, -30],
                    [-30, -40, -40, -50, -50, -40, -40, -30],
                    [-30, -40, -40, -50, -50, -40, -40, -30]]

        '''
        Material basic evaluation:
            Pawn=100
            Bishop=330
            knight=320
            rook=500
            queen=900
            king=20000
        '''

        opp_material = 0
        my_material = 0
        my_b = 0
        opp_b = 0
        for r in range(8):
            for c in range(8):
                piece = board.get_piece(r, c)
                if piece != 0:
                    if piece.get_color() == self.color:
                        if piece.get_symbol().lower() == "p":
                            row, col = piece.get_pos()
                            # reward and penalise positions of pawn according to the scores array
                            if self.is_opposite:
                                my_material += p_scores[row][col]
                            else:
                                my_material += P_scores[row][col]

                            my_material += 100
                        elif piece.get_symbol().lower() == "b":
                            my_material += 330
                            my_b += 1
                            row, col = piece.get_pos()
                            # reward and penalise positions of bishop according to the scores array
                            if self.is_opposite:
                                my_material += b_scores[row][col]
                            else:
                                my_material += B_scores[row][col]

                        elif piece.get_symbol().lower() == "n":
                            my_material += 320
                            row, col = piece.get_pos()
                            # reward and penalise positions of knight according to the scores array
                            if self.is_opposite:
                                my_material += n_scores[row][col]
                            else:
                                my_material += N_scores[row][col]
                        elif piece.get_symbol().lower() == "r":
                            row, col = piece.get_pos()
                            # reward and penalise positions of rook according to the scores array
                            if self.is_opposite:
                                my_material += r_scores[row][col]
                            else:
                                my_material += R_scores[row][col]
                            my_material += 500
                        elif piece.get_symbol().lower() == "q":
                            row, col = piece.get_pos()
                            my_material += 900
                            # reward and penalise positions of queen according to the scores array
                            if self.is_opposite:
                                my_material += q_scores[row][col]
                            else:
                                my_material += Q_scores[row][col]

                        elif piece.get_symbol().lower() == "k":
                            row, col = piece.get_pos()
                            my_material += 20000
                            # reward and penalise positions of king according to the scores array
                            if self.is_opposite:
                                my_material += k_scores[row][col]
                            else:
                                my_material += K_scores[row][col]
                    else:
                        if piece.get_symbol().lower() == "p":
                            row, col = piece.get_pos()
                            # reward and penalise positions of pawn according to the scores array
                            if self.is_opposite:  # then the opponent must be on the close side
                                opp_material += P_scores[row][col]
                            else:
                                opp_material += p_scores[row][col]
                            opp_material += 100
                        elif piece.get_symbol().lower() == "b":
                            row, col = piece.get_pos()
                            opp_material += 330
                            opp_b += 1
                            # reward and penalise positions of bishop according to the scores array
                            if self.is_opposite:  # then the opponent must be on the close side
                                opp_material += B_scores[row][col]
                            else:
                                opp_material += b_scores[row][col]

                        elif piece.get_symbol().lower() == "n":
                            row, col = piece.get_pos()
                            opp_material += 320
                            # reward and penalise positions of knight according to the scores array
                            if self.is_opposite:  # then the opponent must be on the close side
                                opp_material += N_scores[row][col]
                            else:
                                opp_material += n_scores[row][col]

                        elif piece.get_symbol().lower() == "r":
                            row, col = piece.get_pos()
                            opp_material += 500
                            # reward and penalise positions of rook according to the scores array
                            if self.is_opposite:  # then the opponent must be on the close side
                                opp_material += R_scores[row][col]
                            else:
                                opp_material += r_scores[row][col]

                        elif piece.get_symbol().lower() == "q":
                            row, col = piece.get_pos()
                            opp_material += 900
                            # reward and penalise positions of queen according to the scores array
                            if self.is_opposite:  # then the opponent must be on the close side
                                opp_material += Q_scores[row][col]
                            else:
                                opp_material += q_scores[row][col]

                        elif piece.get_symbol().lower() == "k":
                            row, col = piece.get_pos()
                            opp_material += 20000
                            # reward and penalise positions of king according to the scores array
                            if self.is_opposite:  # then the opponent must be on the close side
                                opp_material += K_scores[row][col]
                            else:
                                opp_material += k_scores[row][col]
        # reward bishop pair
        if my_b == 2:
            my_material += 30
        if opp_b == 2:
            opp_material += 30

        material_value = (my_material - opp_material)

        return material_value

    def evaluate_board(self):
        '''
        evaluate a board state. How good it is for the player who's turn it is. Used to evaluate leaf nodes in game tree
        :param opponent: Player object of opponent player
        :return: INTEGER score
        '''
        return self._calculate_material_value(self._board)

    def next_move(self, game):
        '''
        perform move
        :param opponent_player: Player object of the opponent. Used to evaluate leaf nodes and construct game tree
        '''
        opponent = game.get_players()[0] if self.color == "B" else game.get_players()[1]
        # _minimax does push_move and pop_move during traversal which changes half_moves_since_capture and half_moves_since_pawn
        # save the board state
        temp_fen = game.get_fen()
        move = self._minimax(game, self.depth, opponent)[1]
        # set the values to what they were before minimax
        game.load_from_fen(temp_fen)
        self._board.push_move(move)
        if move[0] != "C":  # if move isn't castling
            end_square = (int(move[3]), int(move[4]))
            piece_in_square = self._board.get_piece(end_square[0], end_square[1])
            if piece_in_square.is_pawn:
                if piece_in_square.can_be_promoted():  # if the pawn can be promoted
                    # Promote to Queen by default
                    self._board.push_move(f"P,{end_square[0]}{end_square[1]},Q")

    def _minimax(self, game, depth, opponent_player, alpha=-1e8, beta=+1e8, is_max=True):
        '''
        :param game: Game object
        :param depth: INTEGER
        :param opponent_player: Player object
        :param alpha: INTEGER. Default to large negative number because that's the worst case scenario
        :param beta: INTEGER. Default ot large positive number because that's the worst case scenario
        :param is_max: BOOL. Specify whether the node is a maximiser or a minimiser node.
        :return: best value INTEGER, best move STRING
        '''
        if is_max == True:
            player = self
        else:
            player = opponent_player
        if depth == 0 or opponent_player.is_in_checkmate() or opponent_player.is_stalemate():  # reached end of tree, breaking condition
            return self.evaluate_board(), ""
        best_value = -1e8 if is_max else 1e8
        best_move = ""
        legal_moves = self._board.get_legal_moves(player)
        random.shuffle(legal_moves)  # add randomness

        for move in legal_moves:
            # store the game fen before pushing move
            temp_fen = game.get_fen()
            # perform move
            self._board.push_move(move)
            if move[0] != "C":  # if move isn't castling
                end_square = (int(move[3]), int(move[4]))
                piece_in_square = self._board.get_piece(end_square[0], end_square[1])
                if piece_in_square.is_pawn:
                    if piece_in_square.can_be_promoted():
                        # promote to queen if possible
                        self._board.push_move(f"P,{end_square[0]}{end_square[1]},Q")
            # recursively traverse the child nodes
            eval_child, action_child = self._minimax(game, depth - 1, opponent_player, alpha, beta, not is_max)

            if is_max and best_value < eval_child:
                best_value = eval_child
                best_move = move
                # alpha= the best already explored option for MAX
                alpha = max(alpha, best_value)

            elif (not is_max) and best_value > eval_child:
                best_value = eval_child
                best_move = move
                # beta=the best already explored option for MIN= worst option for MAX
                beta = min(beta, best_value)

            # undoing the move
            game.load_from_fen(temp_fen)

            if beta <= alpha:  # rest can be pruned to save computation
                break
        return best_value, best_move
