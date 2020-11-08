import pygame

PIECE_SIZE = (40, 40)
# loading piece icons
piece_icons = {}
piece_icons["b"] = pygame.transform.scale(pygame.image.load(r"art/bB.png"), PIECE_SIZE)
piece_icons["r"] = pygame.transform.scale(pygame.image.load(r"art/bR.png"), PIECE_SIZE)
piece_icons["n"] = pygame.transform.scale(pygame.image.load(r"art/bKN.png"), PIECE_SIZE)
piece_icons["q"] = pygame.transform.scale(pygame.image.load(r"art/bQ.png"), PIECE_SIZE)
piece_icons["k"] = pygame.transform.scale(pygame.image.load(r"art/bK.png"), PIECE_SIZE)
piece_icons["p"] = pygame.transform.scale(pygame.image.load(r"art/bP.png"), PIECE_SIZE)

piece_icons["B"] = pygame.transform.scale(pygame.image.load(r"art/wB.png"), PIECE_SIZE)
piece_icons["R"] = pygame.transform.scale(pygame.image.load(r"art/wR.png"), PIECE_SIZE)
piece_icons["N"] = pygame.transform.scale(pygame.image.load(r"art/wKN.png"), PIECE_SIZE)
piece_icons["Q"] = pygame.transform.scale(pygame.image.load(r"art/wQ.png"), PIECE_SIZE)
piece_icons["K"] = pygame.transform.scale(pygame.image.load(r"art/wK.png"), PIECE_SIZE)
piece_icons["P"] = pygame.transform.scale(pygame.image.load(r"art/wP.png"), PIECE_SIZE)


class Piece:
    '''
    Parent static class
    '''

    def __init__(self, position, color, board, player):
        '''

        :param position: location of board i.e. (row,col)
        :param color: "W" or "B"
        :param board: Board object
        :param player: Player object
        '''
        self.player = player
        self.is_first_move = True
        self.is_selected = False
        self.row = position[0]
        self.col = position[1]
        self.color = color
        self.is_king = False
        self.is_pawn = False
        self.is_rook = False
        self.is_dead = False
        self.board = board
        self.icon = None

        self.symbol = ""  # white:UPPER  black:lower; pawn->p;bishop->b;knight->n;queen->q;rook->r;king->k

    def get_symbol(self):
        return self.symbol

    # def __repr__(self):
    #     '''
    #     override the default __repr__
    #     :return: symbol of the piece. E.g. P->white Pawn, n->black Knight
    #     '''
    #     return self.symbol

    def select(self):
        self.is_selected = True

    def get_player(self):
        return self.player

    def deselect(self):
        self.is_selected = False

    def change_pos(self, row, col):
        self.row = row
        self.col = col

    def get_pos(self):
        return (self.row, self.col)

    def get_color(self):
        return self.color

    def kill(self):
        self.is_dead = True

    def revive(self):
        self.is_dead = False

    def get_valid_moves(self):
        if self.is_dead:
            return []

    def _filter_moves(self, moves):
        '''
        Protected helper function
        filter our moves that lead to check or don't take the player out of check when they are in check
        so that when doing is_under_attack(),all the opponent's moves are considered.
        :param moves:
        :return: valid moves
        '''

        if self.player.is_turn:
            valid_moves = []
            for move in moves:
                piece_in_square = self.board.get_piece(move[0], move[1])
                if self.is_king:
                    self.player.king_pos = move
                self.board.set_piece(move[0], move[1], self)
                self.board.set_piece(self.row, self.col, 0)
                if not self.board.is_under_attack(self.color, [self.player.king_pos]):
                    valid_moves.append(move)
                if self.is_king:
                    self.player.king_pos = (self.row, self.col)
                self.board.set_piece(self.row, self.col, self)
                self.board.set_piece(move[0], move[1], piece_in_square)
            return valid_moves
        else:
            return moves


class Pawn(Piece):

    def __init__(self, color, position, board, player):
        super().__init__(position, color, board, player)

        self.is_pawn = True
        if self.color == "B":
            self.symbol = "p"
        else:
            self.symbol = "P"
        self.icon = piece_icons[self.symbol]
        self.is_first_move = True if ((self.player.is_opposite and self.row == 1) or (
                    not self.player.is_opposite and self.row == 6)) else False

    def can_be_promoted(self):
        if self.player.is_opposite:
            if self.row == 7 and not self.player.is_in_check():
                return True
            else:
                return False
        elif not self.player.is_opposite:
            if self.row == 0 and not self.player.is_in_check():
                return True
            else:
                return False

    def get_valid_moves(self):
        super().get_valid_moves()
        # TESTED
        self.valid_moves = []
        if self.player.is_opposite == True:
            a = +1
        else:
            a = -1
        self.is_first_move = True if ((self.player.is_opposite and self.row == 1) or (
                    not self.player.is_opposite and self.row == 6)) else False
        # Forward
        if self.is_first_move:
            r = self.row + a
            c = self.col
            if self.board.get_piece(r, c) == 0:
                self.valid_moves.append((r, c))
                r += a
                if r <= 7 and r >= 0 and c <= 7 and c >= 0:
                    if self.board.get_piece(r, c) == 0:
                        self.valid_moves.append((r, c))
        elif not self.is_first_move:
            r = self.row + a
            c = self.col
            if r <= 7 and r >= 0 and c <= 7 and c >= 0:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))

        # diagonals
        # NE
        r = self.row + a
        c = self.col + 1
        if r >= 0 and r <= 7 and c >= 0 and c <= 7:
            if self.board.get_piece(r, c) != 0:
                if self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))

        # NW
        r = self.row + a
        c = self.col - 1
        if r >= 0 and r <= 7 and c >= 0 and c <= 7:
            if self.board.get_piece(r, c) != 0:
                if self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))

        return self._filter_moves(self.valid_moves)


class Knight(Piece):
    def __init__(self, color, position, board, player):
        super().__init__(position, color, board, player)
        if self.color == "B":
            self.symbol = "n"
        else:
            self.symbol = "N"

        self.icon = piece_icons[self.symbol]

    def get_valid_moves(self):

        super().get_valid_moves()
        self.valid_moves = []

        def verify_and_add(row, col):  # helper function
            if (row >= 0 and row <= 7) and (col >= 0 and col <= 7):
                p = self.board.get_piece(row, col)
                if p == 0:
                    self.valid_moves.append((row, col))
                elif p.color != self.color:
                    self.valid_moves.append((row, col))

        # -2,1
        row, col = self.row - 1, self.col - 2
        verify_and_add(row, col)
        # -1,2
        row, col = self.row - 2, self.col - 1
        verify_and_add(row, col)
        # 1,2
        row, col = self.row - 2, self.col + 1
        verify_and_add(row, col)
        # 2,1
        row, col = self.row - 1, self.col + 2
        verify_and_add(row, col)
        # 2,-1
        row, col = self.row + 1, self.col + 2
        verify_and_add(row, col)
        # 1,-2
        row, col = self.row + 2, self.col + 1
        verify_and_add(row, col)
        # -1,-2
        row, col = self.row + 2, self.col - 1
        verify_and_add(row, col)
        # -2,-1
        row, col = self.row + 1, self.col - 2
        verify_and_add(row, col)

        return self._filter_moves(self.valid_moves)


class Bishop(Piece):

    def __init__(self, color, position, board, player):
        super().__init__(position, color, board, player)
        if self.color == "B":
            self.symbol = "b"
        else:
            self.symbol = "B"
        self.icon = piece_icons[self.symbol]

    def get_valid_moves(self, ):

        super().get_valid_moves()
        self.valid_moves = []

        # pos to top left
        end = False
        r = self.row - 1
        c = self.col - 1
        while not end:
            if r >= 0 and c >= 0:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += -1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += -1
                    end = True
                else:
                    end = True
            else:
                end = True

        # pos to bottom right
        r = self.row + 1
        c = self.col + 1
        end = False
        while not end:
            if r <= 7 and c <= 7:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += 1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += 1
                    end = True
                else:
                    end = True
            else:
                end = True

        # bottom left to pos
        r = self.row + 1
        c = self.col - 1
        end = False
        while not end:
            if r >= 0 and c >= 0 and r <= 7 and c <= 7:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += -1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += -1
                    end = True
                else:
                    end = True
            else:
                end = True

        # pos to top right
        r = self.row - 1
        c = self.col + 1
        end = False
        while not end:
            if r >= 0 and c >= 0 and r <= 7 and c <= 7:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += 1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += 1
                    end = True
                else:
                    end = True
            else:
                end = True

        return self._filter_moves(self.valid_moves)


class King(Piece):

    def __init__(self, color, position, board, player):
        super().__init__(position, color, board, player)
        self.is_king = True
        if self.color == "B":
            self.symbol = "k"
        else:
            self.symbol = "K"

        self.icon = piece_icons[self.symbol]

    def get_valid_moves(self):

        super().get_valid_moves()
        self.valid_moves = []

        def verify_and_add(r, c):
            # check the square is in bounds
            if r >= 0 and r <= 7 and c >= 0 and c <= 7:
                p = self.board.get_piece(r, c)
                if p == 0:  # if it's free
                    self.valid_moves.append((r, c))
                elif p.color != self.color:  # if it's enemy
                    self.valid_moves.append((r, c))

        # Top left
        r = self.row - 1
        c = self.col - 1
        verify_and_add(r, c)
        # Top right
        r = self.row - 1
        c = self.col + 1
        verify_and_add(r, c)
        # forward
        r = self.row - 1
        c = self.col
        verify_and_add(r, c)
        # back
        r = self.row + 1
        c = self.col
        verify_and_add(r, c)
        # bottom left
        r = self.row + 1
        c = self.col - 1
        verify_and_add(r, c)
        # bottom right
        r = self.row + 1
        c = self.col + 1
        verify_and_add(r, c)
        # left
        r = self.row
        c = self.col - 1
        verify_and_add(r, c)
        # right
        r = self.row
        c = self.col + 1
        verify_and_add(r, c)

        return self._filter_moves(self.valid_moves)


class Queen(Piece):
    def __init__(self, color, position, board, player):
        super().__init__(position, color, board, player)
        if self.color == "B":
            self.symbol = "q"
        else:
            self.symbol = "Q"
        self.icon = piece_icons[self.symbol]

    def get_valid_moves(self):

        super().get_valid_moves()
        self.valid_moves = []
        # BISHOP moves
        # pos to top left
        end = False
        r = self.row - 1
        c = self.col - 1
        while not end:
            if r >= 0 and c >= 0:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += -1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += -1
                    end = True
                else:
                    end = True
            else:
                end = True

        # pos to bottom right
        r = self.row + 1
        c = self.col + 1
        end = False
        while not end:
            if r <= 7 and c <= 7:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += 1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += 1
                    end = True
                else:
                    end = True
            else:
                end = True

        # bottom left to pos
        r = self.row + 1
        c = self.col - 1
        end = False
        while not end:
            if r >= 0 and c >= 0 and r <= 7 and c <= 7:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += -1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += 1
                    c += -1
                    end = True
                else:
                    end = True
            else:
                end = True

        # pos to top right
        r = self.row - 1
        c = self.col + 1
        end = False
        while not end:
            if r >= 0 and c >= 0 and r <= 7 and c <= 7:
                if self.board.get_piece(r, c) == 0:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += 1
                elif self.board.get_piece(r, c).color != self.color:
                    self.valid_moves.append((r, c))
                    r += -1
                    c += 1
                    end = True
                else:
                    end = True
            else:
                end = True

        # ROOK moves
        # LEFT side
        for i in range(self.col - 1, -1, -1):
            if self.board.get_piece(self.row, i) == 0:
                self.valid_moves.append((self.row, i))
            elif self.board.get_piece(self.row, i).color != self.color:
                self.valid_moves.append((self.row, i))
                break
            else:
                break

        # RIGHT side
        for i in range(self.col + 1, 8):
            if self.board.get_piece(self.row, i) == 0:
                self.valid_moves.append((self.row, i))
            elif self.board.get_piece(self.row, i).color != self.color:
                self.valid_moves.append((self.row, i))
                break
            else:
                break

        # UP
        for i in range(self.row - 1, -1, -1):
            if self.board.get_piece(i, self.col) == 0:
                self.valid_moves.append((i, self.col))
            elif self.board.get_piece(i, self.col).color != self.color:
                self.valid_moves.append((i, self.col))
                break
            else:
                break
        # DOWN
        for i in range(self.row + 1, 8):
            if self.board.get_piece(i, self.col) == 0:
                self.valid_moves.append((i, self.col))
            elif self.board.get_piece(i, self.col).color != self.color:
                self.valid_moves.append((i, self.col))
                break
            else:
                break

        return self._filter_moves(self.valid_moves)


class Rook(Piece):

    def __init__(self, color, position, board, player):
        super().__init__(position, color, board, player)
        self.is_rook = True
        if self.color == "B":
            self.symbol = "r"
        else:
            self.symbol = "R"
        self.icon = piece_icons[self.symbol]

    def get_valid_moves(self):

        super().get_valid_moves()
        self.valid_moves = []
        # LEFT side
        for i in range(self.col - 1, -1, -1):
            if self.board.get_piece(self.row, i) == 0:
                self.valid_moves.append((self.row, i))
            elif self.board.get_piece(self.row, i).color != self.color:
                self.valid_moves.append((self.row, i))
                break
            else:
                break

        # RIGHT side
        for i in range(self.col + 1, 8):
            if self.board.get_piece(self.row, i) == 0:
                self.valid_moves.append((self.row, i))
            elif self.board.get_piece(self.row, i).color != self.color:
                self.valid_moves.append((self.row, i))
                break
            else:
                break

        # UP
        for i in range(self.row - 1, -1, -1):
            if self.board.get_piece(i, self.col) == 0:
                self.valid_moves.append((i, self.col))
            elif self.board.get_piece(i, self.col).color != self.color:
                self.valid_moves.append((i, self.col))
                break
            else:
                break
        # DOWN
        for i in range(self.row + 1, 8):
            if self.board.get_piece(i, self.col) == 0:
                self.valid_moves.append((i, self.col))
            elif self.board.get_piece(i, self.col).color != self.color:
                self.valid_moves.append((i, self.col))
                break
            else:
                break

        return self._filter_moves(self.valid_moves)
