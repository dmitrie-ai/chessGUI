# import all the Piece subclasses
from pieces import *

# constants
BOARD_SIZE = (493, 493)
PIECE_SIZE = (40, 40)
START_OF_BOARD = (20, 30)
START_OF_CELLS = (int(BOARD_SIZE[0] / (10.438) + START_OF_BOARD[0]), int(BOARD_SIZE[0] / (10.438)) + START_OF_BOARD[1])
SQUARE_LENGTH = 50
board_img_path = r"art/chess_board2.gif"
green_overlay_img_path = r"art/green overlay.png"
magenta_overlay_img_path = r"art/magenta overlay.png"
# loading all the art and resizing it to the appropriate dimensions
board_img = pygame.transform.scale(pygame.image.load(board_img_path), BOARD_SIZE)
green_overlay_img = pygame.transform.scale(pygame.image.load(green_overlay_img_path),
                                           (SQUARE_LENGTH, SQUARE_LENGTH))
magenta_overlay_img = pygame.transform.scale(pygame.image.load(magenta_overlay_img_path),
                                             (SQUARE_LENGTH, SQUARE_LENGTH))

# coordinates of each square on the board image ((top left), (top right), (bottom right),(bottom left))
# these have been calculated using the get_square_coordinates() in miscellaneous.py
square_coords = [[[(67, 77), (117, 77), (117, 127), (67, 127)], [(117, 77), (167, 77), (167, 127), (117, 127)],
                  [(167, 77), (217, 77), (217, 127), (167, 127)], [(217, 77), (267, 77), (267, 127), (217, 127)],
                  [(267, 77), (317, 77), (317, 127), (267, 127)], [(317, 77), (367, 77), (367, 127), (317, 127)],
                  [(367, 77), (417, 77), (417, 127), (367, 127)], [(417, 77), (467, 77), (467, 127), (417, 127)]],
                 [[(67, 127), (117, 127), (117, 177), (67, 177)], [(117, 127), (167, 127), (167, 177), (117, 177)],
                  [(167, 127), (217, 127), (217, 177), (167, 177)], [(217, 127), (267, 127), (267, 177), (217, 177)],
                  [(267, 127), (317, 127), (317, 177), (267, 177)], [(317, 127), (367, 127), (367, 177), (317, 177)],
                  [(367, 127), (417, 127), (417, 177), (367, 177)], [(417, 127), (467, 127), (467, 177), (417, 177)]],
                 [[(67, 177), (117, 177), (117, 227), (67, 227)], [(117, 177), (167, 177), (167, 227), (117, 227)],
                  [(167, 177), (217, 177), (217, 227), (167, 227)], [(217, 177), (267, 177), (267, 227), (217, 227)],
                  [(267, 177), (317, 177), (317, 227), (267, 227)], [(317, 177), (367, 177), (367, 227), (317, 227)],
                  [(367, 177), (417, 177), (417, 227), (367, 227)], [(417, 177), (467, 177), (467, 227), (417, 227)]],
                 [[(67, 227), (117, 227), (117, 277), (67, 277)], [(117, 227), (167, 227), (167, 277), (117, 277)],
                  [(167, 227), (217, 227), (217, 277), (167, 277)], [(217, 227), (267, 227), (267, 277), (217, 277)],
                  [(267, 227), (317, 227), (317, 277), (267, 277)], [(317, 227), (367, 227), (367, 277), (317, 277)],
                  [(367, 227), (417, 227), (417, 277), (367, 277)], [(417, 227), (467, 227), (467, 277), (417, 277)]],
                 [[(67, 277), (117, 277), (117, 327), (67, 327)], [(117, 277), (167, 277), (167, 327), (117, 327)],
                  [(167, 277), (217, 277), (217, 327), (167, 327)], [(217, 277), (267, 277), (267, 327), (217, 327)],
                  [(267, 277), (317, 277), (317, 327), (267, 327)], [(317, 277), (367, 277), (367, 327), (317, 327)],
                  [(367, 277), (417, 277), (417, 327), (367, 327)], [(417, 277), (467, 277), (467, 327), (417, 327)]],
                 [[(67, 327), (117, 327), (117, 377), (67, 377)], [(117, 327), (167, 327), (167, 377), (117, 377)],
                  [(167, 327), (217, 327), (217, 377), (167, 377)], [(217, 327), (267, 327), (267, 377), (217, 377)],
                  [(267, 327), (317, 327), (317, 377), (267, 377)], [(317, 327), (367, 327), (367, 377), (317, 377)],
                  [(367, 327), (417, 327), (417, 377), (367, 377)], [(417, 327), (467, 327), (467, 377), (417, 377)]],
                 [[(67, 377), (117, 377), (117, 427), (67, 427)], [(117, 377), (167, 377), (167, 427), (117, 427)],
                  [(167, 377), (217, 377), (217, 427), (167, 427)], [(217, 377), (267, 377), (267, 427), (217, 427)],
                  [(267, 377), (317, 377), (317, 427), (267, 427)], [(317, 377), (367, 377), (367, 427), (317, 427)],
                  [(367, 377), (417, 377), (417, 427), (367, 427)], [(417, 377), (467, 377), (467, 427), (417, 427)]],
                 [[(67, 427), (117, 427), (117, 477), (67, 477)], [(117, 427), (167, 427), (167, 477), (117, 477)],
                  [(167, 427), (217, 427), (217, 477), (167, 477)], [(217, 427), (267, 427), (267, 477), (217, 477)],
                  [(267, 427), (317, 427), (317, 477), (267, 477)], [(317, 427), (367, 427), (367, 477), (317, 477)],
                  [(367, 427), (417, 427), (417, 477), (367, 477)], [(417, 427), (467, 427), (467, 477), (417, 477)]]]


class Board:
    def __init__(self,
                 game_display):  # game_display: object of pygame.display. It allows the class to draw onto the display
        self.pieces = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(8)]  # 8x8 array with default value of 0
        self.game_display = game_display
        self.moves_displayed = False  # indicate whether valid moves are being displayed onto the screen
        self._corner_coords = None  # corner coordinates used in other methods to save computation by not updating whole screen
        self._selected_piece = None  # the piece selected before the current one
        self._castling_mode = False  # indicates whether the castling squares are dispalyed
        # number of half moves since the last capture or pawn advance. Used to check whether a draw can be claimed via the 50 move rule
        self.half_moves_since_capture_or_p_advance = 0

    def set_castling_mode(self, value):
        '''
        :param value: Boolean
        '''
        self._castling_mode = value

    def replace(self, old_piece, new_piece):
        '''
        :param old_piece: Piece object
        :param new_piece: Piece object
        '''
        self.pieces[old_piece.get_pos()[0]][old_piece.get_pos()[1]] = new_piece
        del old_piece  # delete the object to free memory

    def get_pieces(self):
        return self.pieces

    def is_under_attack(self, color, square_list):
        '''
        color=the player's color(not the opponent)="W"|"B";
        square_list= squares((row,col) e.g. (1,2))) to check if they are under attack by the opponent.
        Return True if any of the squares in square_list is under attack by teh opponent
        '''
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece != 0:
                    if piece.get_color() != color:  # if it is the opponent's piece
                        valid_moves = piece.get_valid_moves()
                        for sq in square_list:
                            if sq in valid_moves:
                                return True
        return False

    def get_selected_piece(self):
        return self._selected_piece

    def set_selected_piece(self, piece):
        self._selected_piece = piece

    def get_castling_mode(self):
        return self._castling_mode

    def get_piece(self, row, col):
        return self.pieces[row][col]

    def set_piece(self, row, col, piece):  # takes Piece object or 0 if no piece
        self.pieces[row][col] = piece

    def can_castle(self, player):  # player=Player object
        # checks whether player can castle and which sided the player can castle

        king = self.get_piece(player.king_pos[0], player.king_pos[1])  # gets the player's king
        if not king.is_first_move:
            return {"K": False, "Q": False}
        if player.is_in_check():
            return {"K": False, "Q": False}
        if player.is_opposite:

            left_rook = self.get_piece(0, 0)
            right_rook = self.get_piece(0, 7)
            king_side = False
            queen_side = False
            # check bishop side castling option
            if right_rook != 0:
                if right_rook.is_rook:
                    if right_rook.is_first_move:
                        if player.get_color() == "W":
                            squares_to_check = [(0, 1), (0, 2)]
                        else:
                            squares_to_check = [(0, 5), (0, 6)]
                        if self.get_piece(squares_to_check[0][0],
                                          squares_to_check[0][1]) == 0 and self.get_piece(
                            squares_to_check[1][0], squares_to_check[1][1]) == 0:
                            # check if the squares through which the king would pass are under attack
                            if self.is_under_attack(player.get_color(), squares_to_check) == False:
                                king_side = True
            # check queen side
            if left_rook != 0:
                if left_rook.is_rook:
                    if left_rook.is_first_move:
                        if player.get_color() == "W":
                            squares_to_check = [(0, 4), (0, 5)]
                        else:
                            squares_to_check = [(0, 2), (0, 3)]

                        if self.get_piece(squares_to_check[0][0],
                                          squares_to_check[0][1]) == 0 and self.get_piece(
                            squares_to_check[1][0], squares_to_check[1][1]) == 0:
                            # check if the squares through which the king would pass are under attack
                            if self.is_under_attack(player.get_color(), squares_to_check) == False:
                                queen_side = True

        else:
            left_rook = self.get_piece(7, 0)
            right_rook = self.get_piece(7, 7)
            king_side = False
            queen_side = False
            # check bishop side castling option

            if right_rook != 0:
                if right_rook.is_rook:
                    if right_rook.is_first_move:
                        if player.get_color() == "W":
                            squares_to_check = [(7, 6), (7, 5)]
                        else:
                            squares_to_check = [(7, 1), (7, 2)]
                        if self.get_piece(squares_to_check[0][0],
                                          squares_to_check[0][1]) == 0 and self.get_piece(
                            squares_to_check[1][0], squares_to_check[1][1]) == 0:
                            # check if the squares through which the king would pass are under attack
                            if self.is_under_attack(player.get_color(), squares_to_check) == False:
                                king_side = True

            # check queen side castling option

            if left_rook != 0:
                if left_rook.is_rook:
                    if left_rook.is_first_move:
                        if player.get_color() == "W":
                            squares_to_check = [(7, 2), (7, 3)]
                        else:
                            squares_to_check = [(7, 4), (7, 5)]

                        if self.get_piece(squares_to_check[0][0],
                                          squares_to_check[0][1]) == 0 and self.get_piece(
                            squares_to_check[1][0], squares_to_check[1][1]) == 0:
                            # check if the squares through which the king would pass are under attack
                            if self.is_under_attack(player.get_color(), squares_to_check) == False:
                                queen_side = True

        return {"K": king_side, "Q": queen_side}

    def draw_castling_squares(self, player):
        # draws the castling squares
        if player.is_opposite:
            # the squares that need to be lit when castling mode  {"K":[(if white) ,(if black) ],"Q":[(if white),(if black)]}
            temp = {"K": [(0, 1), (0, 6)], "Q": [(0, 5), (0, 2)]}
        else:
            temp = {"K": [(7, 6), (7, 1)], "Q": [(7, 2), (7, 5)]}

        squares = []
        draw = False
        can_castle = self.can_castle(player)
        if can_castle["K"]:
            draw = True
            if player.get_color() == "W":
                squares.append(temp["K"][0])
            elif player.get_color() == "B":
                squares.append(temp["K"][1])
        if can_castle["Q"]:
            draw = True
            if player.get_color() == "W":
                squares.append(temp["Q"][0])
            elif player.get_color() == "B":
                squares.append(temp["Q"][1])
        if draw:
            self._selected_piece = None
            self._castling_mode = True
            self.draw_green_squares(squares)
        return squares  # save computation later

    def get_legal_moves(self, player):
        '''
        get all the legal moves of player
        :param player: Player object
        :return:
        '''
        legal_moves = []
        if self.can_castle(player)["Q"]:
            legal_moves.append(f'C,{player.king_pos[0]}{player.king_pos[1]},Q')
        if self.can_castle(player)["K"]:
            legal_moves.append(f'C,{player.king_pos[0]}{player.king_pos[1]},K')

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece != 0:
                    if piece.get_color() == player.get_color():
                        valid_moves = piece.get_valid_moves()
                        if valid_moves != []:
                            for move in valid_moves:
                                legal_moves.append(f'{piece.get_pos()[0]}{piece.get_pos()[1]},{move[0]}{move[1]}')

        return legal_moves

    def create_board(self, white_player, black_player):
        # initialise board at the start of a game
        if black_player.is_opposite:
            opposite_player = black_player
            close_player = white_player
        else:
            opposite_player = white_player
            close_player = black_player

        # opposite
        self.pieces[0][0] = Rook(opposite_player.get_color(), (0, 0), self, opposite_player)
        self.pieces[0][1] = Knight(opposite_player.get_color(), (0, 1), self, opposite_player)
        self.pieces[0][2] = Bishop(opposite_player.get_color(), (0, 2), self, opposite_player)
        if opposite_player.get_color() == "W":
            self.pieces[0][3] = King(opposite_player.get_color(), (0, 3), self, opposite_player)
            self.pieces[0][4] = Queen(opposite_player.get_color(), (0, 4), self, opposite_player)
        else:
            self.pieces[0][3] = Queen(opposite_player.get_color(), (0, 3), self, opposite_player)
            self.pieces[0][4] = King(opposite_player.get_color(), (0, 4), self, opposite_player)
        self.pieces[0][5] = Bishop(opposite_player.get_color(), (0, 5), self, opposite_player)
        self.pieces[0][6] = Knight(opposite_player.get_color(), (0, 6), self, opposite_player)
        self.pieces[0][7] = Rook(opposite_player.get_color(), (0, 7), self, opposite_player)
        # opposite pawns
        for y in range(8):
            self.pieces[1][y] = Pawn(opposite_player.get_color(), (1, y), self, opposite_player)
        # close pieces
        self.pieces[7][0] = Rook(close_player.get_color(), (7, 0), self, close_player)
        self.pieces[7][1] = Knight(close_player.get_color(), (7, 1), self, close_player)
        self.pieces[7][2] = Bishop(close_player.get_color(), (7, 2), self, close_player)
        if close_player.get_color() == "W":

            self.pieces[7][3] = Queen(close_player.get_color(), (7, 3), self, close_player)
            self.pieces[7][4] = King(close_player.get_color(), (7, 4), self, close_player)
        else:
            self.pieces[7][3] = King(close_player.get_color(), (7, 3), self, close_player)
            self.pieces[7][4] = Queen(close_player.get_color(), (7, 4), self, close_player)
        self.pieces[7][5] = Bishop(close_player.get_color(), (7, 5), self, close_player)
        self.pieces[7][6] = Knight(close_player.get_color(), (7, 6), self, close_player)
        self.pieces[7][7] = Rook(close_player.get_color(), (7, 7), self, close_player)
        # close pawns
        for y in range(8):
            self.pieces[6][y] = Pawn(close_player.get_color(), (6, y), self, close_player)

    def __repr__(self):
        '''
        override the default method __repr__() so that it returns the board in text form
        helps to troubleshoot and test
        Example:
        |0|0|k|r|0|0|0|r|
        |p|b|q|p|b|p|p|p|
        |n|0|p|0|0|0|0|n|
        |0|p|0|0|p|0|0|0|
        |0|P|P|0|P|0|0|0|
        |N|0|0|0|0|0|0|N|
        |P|B|Q|P|B|P|P|P|
        |0|0|K|R|0|0|0|R|
        '''
        whole_string = ''''''
        for row in range(8):
            row_string = "|"
            for column in range(8):
                if self.pieces[row][column] == 0:
                    symbol = "0"
                else:
                    piece = self.pieces[row][column]
                    symbol = piece.get_symbol()
                row_string += f"{symbol}|"
            whole_string = f"{whole_string}{row_string}\n"
        return whole_string

    def draw_board(self):  # Draw board with pieces on it
        self.game_display.blit(board_img, START_OF_BOARD)
        board = self.pieces
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece != 0:
                    row = piece.row
                    col = piece.col
                    icon = piece.icon
                    # draws each piece's icon in the right square with 5px padding left and top
                    self.game_display.blit(icon, (square_coords[row][col][0][0] + 5, square_coords[row][col][0][1] + 5))

    def get_square(self, x, y):
        '''
        returns the row and col of the square that includes the given coordinates
        :param x: cartesian x coordinate
        :param y: cartesian y cordiante; top left is (0,0)
        :return: (row,column) where the coordinates are located or None if the coordinates are not on any square
        '''
        row = None
        col = None
        # find the col
        for i in range(8):
            s = square_coords[0][i]
            left_x = s[0][0]
            right_x = s[1][0]

            if x >= left_x and x < right_x:
                col = i
                break

        # find the row
        for i in range(8):
            top = START_OF_CELLS[1] + (SQUARE_LENGTH * i)
            bottom = START_OF_CELLS[1] + (SQUARE_LENGTH * (i + 1))
            if y >= top and y < bottom:
                row = i
                break
        if row == None or col == None:
            return None
        else:
            return (row, col)

    def update_squares(self, whole=False):
        '''
        Improve performance by only updating squares that have been last drawn on
        :param whole: if the whole diplay has to be updated
        '''
        if not whole:
            if self._corner_coords != [] and self._corner_coords != None:
                dirty_rects = []
                for coord in self._corner_coords:
                    dirty_rects.append(pygame.Rect(coord[0], coord[1], SQUARE_LENGTH, SQUARE_LENGTH))

                pygame.display.update(dirty_rects)
        else:
            pygame.display.update()

    def draw_green_squares(self, squares):
        '''
        draws the green_overlay_img on the given square
        :param squares: list of squares (row,col) on which to draw
        '''
        self._corner_coords = self.draw_overlay(squares, green_overlay_img)

    def draw_magenta_squares(self, squares):
        '''
        draws the magenta_overlay_img on the given square
        :param squares: list of squares (row,col) on which to draw
        '''
        self.draw_overlay(squares, magenta_overlay_img)

    def draw_overlay(self, squares, image):
        '''
        Draw image on particular squares
        :param squares: list of squares (row,col) on which to draw
        :param image: the pygame.image object
        :return: the coordinates of teh top left corner of the squares on which it has been draw.
        Improves performance when updating th display
        '''
        corner_coords = []
        for square in squares:
            pos = square_coords[square[0]][square[1]][0]
            corner_coords.append(pos)
            self.game_display.blit(image, pos)
        return corner_coords

    def push_move(self, move):
        '''
        Format of moves
        "start_square,end_square"->the piece in start_square moves to end_square; E.g. "01,11"
        "P,square,Q"->promote the piece in square to Queen
        "P,square,N"->promote the piece in square to Knight
        "P,square,R"->promote the piece in square to Knight
        "P,square,B"->promote the piece in square to Knight
        "C,king_pos,Q"->castle Queen side. original king position = king_pos
        "C,king_pos,K"->castle king side
        '''
        parts = move.split(",")

        if parts[0] == "C":
            king = self.get_piece(int(parts[1][0]), int(parts[1][1]))
            player = king.get_player()
            player.castle(parts[2])
            self.half_moves_since_capture_or_p_advance = 0

        elif parts[0] == "P":
            piece = self.get_piece(int(parts[1][0]), int(parts[1][1]))
            promote_to = parts[2]
            if promote_to == "Q":
                new_q_piece = Queen(piece.get_color(), piece.get_pos(), self, piece.get_player())
                self.replace(piece, new_q_piece)
            elif promote_to == "N":
                new_kn_piece = Knight(piece.get_color(), piece.get_pos(), self, piece.get_player())
                self.replace(piece, new_kn_piece)
            elif promote_to == "R":
                new_r_piece = Rook(piece.get_color(), piece.get_pos(), self, piece.get_player())
                self.replace(piece, new_r_piece)
            elif promote_to == "B":
                new_b_piece = Bishop(piece.get_color(), piece.get_pos(), self, piece.get_player())
                self.replace(piece, new_b_piece)

        else:
            piece = self.get_piece(int(parts[0][0]), int(parts[0][1]))
            start_square = (int(parts[0][0]), int(parts[0][1]))
            end_square = (int(parts[1][0]), int(parts[1][1]))

            if piece.is_first_move:
                piece.is_first_move = False

            if piece.is_king:
                piece.get_player().king_pos = end_square
            piece_in_new_square = self.get_piece(end_square[0], end_square[1])
            if piece_in_new_square != 0:  # if the move involves catpure
                self.half_moves_since_capture_or_p_advance = 0
                piece.get_player().captured_pieces.append(piece_in_new_square)
                piece_in_new_square.kill()
            else:
                if not piece.is_pawn:
                    self.half_moves_since_capture_or_p_advance += 1

            self.set_piece(start_square[0], start_square[1], 0)
            self.set_piece(end_square[0], end_square[1], piece)
            piece.change_pos(end_square[0], end_square[1])