from widgets import Button, Label
# import Stockfish class and the helper functions
from stockfish_parser import *
from chess_board import *
import pygame
from miscellaneous import *
from player import PlayerHuman, PlayerStockfish, PlayerAI

# define some colour for clarity
black = (0, 0, 0)
red = (255, 0, 0)
green = (212, 235, 20)
magenta = (235, 20, 212)
blue = (20, 212, 235)
white = (255, 255, 255)
# default AI-tip depth
AI_tip_depth = 16
# default font
font = "comicsansms"


class HumanVsHumanGame():
    def __init__(self, playerW, playerB, board, game_display):
        '''
        :param playerW: Player object. White player
        :param playerB: Player object. Black player
        :param board: Board object
        :param game_display: pygame.display object. Allows the class to draw onto the display
        '''
        self.game_display = game_display
        self.board = board
        self.playerW = playerW
        self.playerB = playerB
        self.white_label = Label("WHITE", blue, 230, 0, 20)
        self.black_label = Label("BLACK", blue, 230, 0, 20)
        self.check_label = Label("CHECK", red, 225, 523, 25)
        self.checkmate_label = Label("CHECKMATE", red, 200, 523, 25)
        self.stalemate_label = Label("STALEMATE", red, 200, 523, 25)
        self.draw_label = Label("50 move Draw", red, 190, 523, 25)
        self.castle_btn = Button(438, 523, 75, 30, green, "CASTLE", magenta, font_size=18)
        self.undo_btn = Button(20, 523, 60, 30, green, "UNDO", magenta, font_size=18)
        self.AI_tip_btn = Button(374, 523, 60, 30, green, "AI Tip", magenta, font_size=18)
        self.to_menu_btn = Button(0, 0, 50, 30, green, "Back", magenta)
        self.fen_stack = []  # fen string added after each player's turn.

        if self.playerB.is_opposite:
            start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        else:
            # if white is on the opposite side of the board, switch the king and queen around so that the arrangement is correct
            start_fen = 'rnbkqbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBKQBNR w KQkq - 0 1'
        self.fen_stack.append(start_fen)
        self.half_moves = 0
        self.current_player = self.playerW
        self.quit_game = False
        self._can_en_passant = False  # False or the position of the passing square where teh capturing piece would end up. One square behind the pawn that advanced 2 squares

    def get_players(self):  # [white_player,black_player]
        return [self.playerW, self.playerB]

    def check_draw(self):  # Check if a draw can be claimed by the 50 move rule
        if self.board.half_moves_since_capture_or_p_advance / 2 >= 50:
            return True
        else:
            return False

    def en_passant(self, capturing_piece):
        if self._can_en_passant[0] == 2:  # if opposite player has opened up to en passant
            captured_piece = self.board.get_piece(3, self._can_en_passant[1])
            self.board.set_piece(3, self._can_en_passant[1], 0)  # remove the captured piece
        else:  # if the close player has opened up to en passant
            captured_piece = self.board.get_piece(4, self._can_en_passant[1])
            self.board.set_piece(4, self._can_en_passant[1], 0)
        captured_piece.kill()
        self.board.half_moves_since_capture_or_p_advance = 0
        self.current_player.captured_pieces.append(captured_piece)
        self.board.set_piece(capturing_piece.get_pos()[0], capturing_piece.get_pos()[1], 0)
        self.board.set_piece(self._can_en_passant[0], self._can_en_passant[1], capturing_piece)
        capturing_piece.change_pos(self._can_en_passant[0], self._can_en_passant[1])

    def load_from_fen(self, fen):  # load a fen position, used in UNDO feature
        split_fen = fen.split(" ")  # list of the fen string parts
        # arrange the board
        rows = split_fen[0].split("/")
        if self.playerB.is_opposite:  # if the black player is opposite
            for r, row in enumerate(rows):
                current_col = 0
                for char in row:
                    if char.isdigit():
                        for i in range(int(char)):
                            self.board.set_piece(r, current_col, 0)
                            current_col += 1
                    else:
                        if char.lower() == "p":
                            self.board.set_piece(r, current_col,
                                                 Pawn("B" if char.islower() else "W", (r, current_col), self.board,
                                                      self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "n":
                            self.board.set_piece(r, current_col,
                                                 Knight("B" if char.islower() else "W", (r, current_col), self.board,
                                                        self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "b":
                            self.board.set_piece(r, current_col,
                                                 Bishop("B" if char.islower() else "W", (r, current_col), self.board,
                                                        self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "r":
                            self.board.set_piece(r, current_col,
                                                 Rook("B" if char.islower() else "W", (r, current_col), self.board,
                                                      self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "q":
                            self.board.set_piece(r, current_col,
                                                 Queen("B" if char.islower() else "W", (r, current_col), self.board,
                                                       self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "k":
                            self.board.set_piece(r, current_col,
                                                 King("B" if char.islower() else "W", (r, current_col), self.board,
                                                      self.playerB if char.islower() else self.playerW))
                            if char.islower():
                                self.playerB.king_pos = (r, current_col)
                            else:
                                self.playerW.king_pos = (r, current_col)
                        current_col += 1
        else:  # if the white is on the opposite side
            rows.reverse()  # FEN strings are always from teh perspective of black on the opposite side
            for r, row in enumerate(rows):
                current_col = 0
                for char in row:
                    if char.isdigit():
                        for i in range(int(char)):
                            self.board.set_piece(r, current_col, 0)
                            current_col += 1
                    else:
                        if char.lower() == "p":
                            self.board.set_piece(r, current_col,
                                                 Pawn("B" if char.islower() else "W", (r, current_col), self.board,
                                                      self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "n":
                            self.board.set_piece(r, current_col,
                                                 Knight("B" if char.islower() else "W", (r, current_col), self.board,
                                                        self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "b":
                            self.board.set_piece(r, current_col,
                                                 Bishop("B" if char.islower() else "W", (r, current_col), self.board,
                                                        self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "r":
                            self.board.set_piece(r, current_col,
                                                 Rook("B" if char.islower() else "W", (r, current_col), self.board,
                                                      self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "q":
                            self.board.set_piece(r, current_col,
                                                 Queen("B" if char.islower() else "W", (r, current_col), self.board,
                                                       self.playerB if char.islower() else self.playerW))
                        elif char.lower() == "k":
                            self.board.set_piece(r, current_col,
                                                 King("B" if char.islower() else "W", (r, current_col), self.board,
                                                      self.playerB if char.islower() else self.playerW))
                            if char.islower():
                                self.playerB.king_pos = (r, current_col)
                            else:
                                self.playerW.king_pos = (r, current_col)
                        current_col += 1

        # set up which player's turn it is
        if split_fen[1] == "w":
            self.current_player = self.playerW
            self.playerW.is_turn = True
            self.playerB.is_turn = False
        elif split_fen[1] == "b":
            self.current_player = self.playerB
            self.playerW.is_turn = False
            self.playerB.is_turn = True

        # castling rights
        if split_fen[2] == "-":
            self.board.get_piece(self.playerW.king_pos[0], self.playerW.king_pos[1]).is_first_move = False
            self.board.get_piece(self.playerB.king_pos[0], self.playerB.king_pos[1]).is_first_move = False
        else:
            for x in split_fen[2]:
                if x == "K":
                    self.board.get_piece(self.playerW.king_pos[0], self.playerW.king_pos[1]).is_first_move = True
                    if self.playerW.is_opposite:
                        self.board.get_piece(0, 0).is_first_move = True
                    else:
                        self.board.get_piece(7, 7).is_first_move = True
                elif x == "Q":
                    self.board.get_piece(self.playerW.king_pos[0], self.playerW.king_pos[1]).is_first_move = True
                    if self.playerW.is_opposite:
                        self.board.get_piece(0, 7).is_first_move = True
                    else:
                        self.board.get_piece(7, 0).is_first_move = True
                elif x == "k":
                    self.board.get_piece(self.playerB.king_pos[0], self.playerB.king_pos[1]).is_first_move = True
                    if self.playerB.is_opposite:
                        self.board.get_piece(0, 7).is_first_move = True
                    else:
                        self.board.get_piece(7, 0).is_first_move = True
                elif x == "q":
                    self.board.get_piece(self.playerB.king_pos[0], self.playerB.king_pos[1]).is_first_move = True
                    if self.playerB.is_opposite:
                        self.board.get_piece(0, 0).is_first_move = True
                    else:
                        self.board.get_piece(7, 7).is_first_move = True
        # en_passant
        if split_fen[3] == "-":
            self._can_en_passant = False
        else:
            self._can_en_passant = algebraic_to_array_form(split_fen[3])
        # half moves since capture or pawn advance
        self.board.half_moves_since_capture_or_p_advance = int(split_fen[4])
        # total half moves
        if self.current_player == self.playerW:
            # if it is white's turn then a full move has been performed
            self.half_moves = int(int(split_fen[5]) * 2) - 2
        else:
            # if it is black's turn, the move is not over
            self.half_moves = int(int(split_fen[5]) * 2) - 1

    def show_en_passant(self):
        '''
        Show the en-pasant capture menu and allow the user to choose whether to en-passant capture or not
        '''
        l1 = Label("En-passant capture?", blue, 540, 250, 25)
        l1.draw(self.game_display)
        yes_btn = Button(590, 290, 50, 35, green, "Yes", magenta)
        no_btn = Button(670, 290, 50, 35, green, "No", magenta)
        yes_btn.draw(self.game_display)
        no_btn.draw(self.game_display)
        l1.update()
        yes_btn.update()
        no_btn.update()
        en_passant_mode = True
        while en_passant_mode:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if yes_btn.is_over(mouse_pos):
                        en_passant_mode = False
                        self.erase_widgets([l1, yes_btn, no_btn])
                        return True
                    if no_btn.is_over(mouse_pos):
                        en_passant_mode = False
                        self.erase_widgets([l1, yes_btn, no_btn])
                        return False
                # if the cross top right is clicked
                if event.type == pygame.QUIT:
                    exit = True
                    self.quit()

    # FEN representation of a state   https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation; white:Upper;   black:lower
    def get_fen(self):
        fen_rows = []
        # arrangement of pieces
        for r in range(8):
            row_fen = ""
            zero_counter = 0
            for c in range(8):
                piece = self.board.get_piece(r, c)
                if piece != 0:
                    if zero_counter != 0:
                        row_fen += str(zero_counter)
                    zero_counter = 0
                    row_fen += piece.get_symbol()
                else:
                    zero_counter += 1
            if zero_counter != 0:
                row_fen += str(zero_counter)

            fen_rows.append(row_fen)
        # FEN is always from the perspective of black being opposite of the board and white being close. To allow for black to be the close player.
        if self.playerW.is_opposite:
            fen_rows.reverse()
        fen = "/".join(fen_rows)
        # add the colour indicator
        fen += f" {self.current_player.get_color().lower()}"
        # Castling rights
        castling_rights_fen = ""
        if self.board.get_piece(self.playerW.king_pos[0], self.playerW.king_pos[1]).is_first_move:
            if not self.playerW.is_opposite:
                bottom_left_piece = self.board.get_piece(7, 0)
                if bottom_left_piece != 0:
                    if bottom_left_piece.get_symbol() == "R":
                        if bottom_left_piece.is_first_move:
                            castling_rights_fen += "Q"
                bottom_right_piece = self.board.get_piece(7, 7)
                if bottom_right_piece != 0:
                    if bottom_right_piece.get_symbol() == "R":
                        if bottom_right_piece.is_first_move:
                            castling_rights_fen += "K"
            elif self.playerW.is_opposite:
                top_left = self.board.get_piece(0, 0)
                if top_left != 0:

                    if top_left.get_symbol() == "R":
                        if top_left.is_first_move:
                            castling_rights_fen += "K"
                top_right = self.board.get_piece(0, 7)
                if top_right != 0:
                    if top_right.get_symbol() == "R":
                        if top_right.is_first_move:
                            castling_rights_fen += "Q"
        if self.board.get_piece(self.playerB.king_pos[0], self.playerB.king_pos[1]).is_first_move:
            if not self.playerB.is_opposite:
                bottom_left_piece = self.board.get_piece(7, 0)
                if bottom_left_piece != 0:
                    if bottom_left_piece.get_symbol() == "r":
                        if bottom_left_piece.is_first_move:
                            castling_rights_fen += "k"
                bottom_right_piece = self.board.get_piece(7, 7)
                if bottom_right_piece != 0:
                    if bottom_right_piece.get_symbol() == "r":
                        if bottom_right_piece.is_first_move:
                            castling_rights_fen += "q"
            elif self.playerB.is_opposite:
                top_left = self.board.get_piece(0, 0)
                if top_left != 0:
                    if top_left.get_symbol() == "r":
                        if top_left.is_first_move:
                            castling_rights_fen += "q"
                top_right = self.board.get_piece(0, 7)
                if top_right != 0:
                    if top_right.get_symbol() == "r":
                        if top_right.is_first_move:
                            castling_rights_fen += "k"
        if castling_rights_fen == "":
            castling_rights_fen = "-"
        fen += f' {castling_rights_fen}'
        # en passant
        if self._can_en_passant == False:
            fen += f' -'
        else:
            fen += f' {array_to_algebraic_form(self._can_en_passant)}'
        # halfmoves since last capture or pawn advance
        fen += f' {self.board.half_moves_since_capture_or_p_advance}'
        # full moves
        fen += f' {int((self.half_moves) / 2) + 1}'
        return fen

    def go_to_main(self):  # whenever the back button is clicked whilst in game
        menu(self.game_display)

    def get_best_move(self, depth):  # also converts from algebraic notation to the notation used in the program
        stockfish = init_stockfish(depth)
        move = get_best_move(stockfish, self.get_fen())
        if move == "O-O":  # King side castling
            move = f'C,{self.current_player.king_pos[0]}{self.current_player.king_pos[1]},K'
            return move
        elif move == "O-O-O":  # Queen side castling
            move = f'C,{self.current_player.king_pos[0]}{self.current_player.king_pos[1]},Q'
            return move
        else:
            start_pos = algebraic_to_array_form(move[:2])
            end_pos = algebraic_to_array_form(move[2:])
            if self.playerW.is_opposite:
                # the best move is given assuming that white is the close player and black is the opposite player
                # reflects the move so that it works with white being opposite
                start_pos = (-start_pos[0] + 7, start_pos[1])
                end_pos = (-end_pos[0] + 7, end_pos[1])
            return f'{start_pos[0]}{start_pos[1]},{end_pos[0]}{end_pos[1]}'

    def show_best_move(self, depth=AI_tip_depth):
        best_move = self.get_best_move(depth)
        if best_move[0] == "C":
            side = best_move[5]
            tip = f'Castling {side} side'
        else:
            start_pos = (int(best_move[0]), int(best_move[1]))
            end_pos = (int(best_move[3]), int(best_move[4]))
            tip = f'{array_to_algebraic_form(start_pos)}{array_to_algebraic_form(end_pos)}'
            self.board.draw_magenta_squares([start_pos, end_pos])

        AI_tip_label = Label(tip, red, 530, 250, 60)
        AI_tip_label.draw(self.game_display)
        pygame.display.update()
        drawn = True
        while drawn:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    AI_tip_label.erase(self.game_display)
                    self.board.draw_board()
                    pygame.display.update()
                    drawn = False
                    break
                # if the user clicks the cross top right
                if event.type == pygame.QUIT:
                    self.quit_game = True
                    self.quit()

    def _end_of_turn(self):
        '''
        Used to display check , stalemate and checkmate labels appropriately after each turn
        '''
        self.fen_stack.append(self.get_fen())  # add the fen to the stack after each player's turn
        if self.current_player.is_stalemate():
            self.stalemate_label.draw(self.game_display)
            self.stalemate_label.update()
        elif self.current_player.is_in_checkmate():
            self.checkmate_label.draw(self.game_display)
            self.checkmate_label.update()
        elif self.current_player.is_in_check():
            self.check_label.draw(self.game_display)
            self.check_label.update()
        elif self.check_draw():
            self.draw_label.draw(self.game_display)
            self.draw_label.update()
        else:
            # this erases the check label, sstalemate label, checkmate label because it just redraws that region of space
            self.checkmate_label.erase(self.game_display)

    # Main game loop
    def start(self):
        self.board.create_board(self.playerW, self.playerB)  # initialise the board
        self.board.draw_board()
        self.draw_player_label()
        self.castle_btn.draw(self.game_display)
        self.undo_btn.draw(self.game_display)
        self.AI_tip_btn.draw(self.game_display)
        self.to_menu_btn.draw(self.game_display)
        pygame.display.update()

        while not self.quit_game:

            for event in pygame.event.get():
                # Handling mouse clicks and position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    # if undo button is pressed
                    if self.undo_btn.is_over(mouse_pos) and self.half_moves >= 1:
                        self.undo()
                        self.board.draw_board()
                        self.checkmate_label.erase(self.game_display)
                        self.draw_player_label()
                        self.board.update_squares(whole=True)

                    # castling button
                    elif self.to_menu_btn.is_over(mouse_pos):
                        self.go_to_main()
                        break
                    elif self.castle_btn.is_over(mouse_pos):
                        if self.board.get_castling_mode():  # if the buttons has been pressed before
                            self.board.set_castling_mode(False)
                            self.board.set_selected_piece(None)
                            self.board.draw_board()
                        else:
                            squares = self.board.draw_castling_squares(self.current_player)
                        self.board.update_squares(squares)
                    elif self.AI_tip_btn.is_over(mouse_pos):
                        self.show_best_move()
                    else:
                        # (row, col) of the clicked square
                        clicked_square = self.board.get_square(mouse_pos[0], mouse_pos[1])
                        if self.board.get_castling_mode() and clicked_square in squares:
                            king_pos = self.current_player.king_pos
                            # perform castling
                            if clicked_square[1] < 4:
                                if self.current_player.is_opposite:
                                    if self.current_player.get_color() == "W":
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                    else:
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")
                                else:
                                    if self.current_player.get_color() == "W":
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")
                                    else:
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                            else:
                                if self.current_player.is_opposite:
                                    if self.current_player.get_color() == "W":
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")
                                    else:
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                else:
                                    if self.current_player.get_color() == "W":
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                    else:
                                        self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")

                            self.board.update_squares(whole=True)
                            self.half_moves += 1
                            self.current_player.is_turn = False
                            self.current_player = self.playerW if self.current_player == self.playerB else self.playerB
                            self.current_player.is_turn = True
                            self.draw_player_label()
                            self._end_of_turn()  # add fen to fen stack and display check checkmate and stalemate labels appropriately

                        elif clicked_square is not None:
                            piece = self.board.get_piece(clicked_square[0], clicked_square[1])
                            # moving pieces
                            if self.board.moves_displayed:
                                valid_moves = self.board.get_selected_piece().get_valid_moves()
                                if clicked_square in valid_moves:
                                    selected_piece = self.board.get_selected_piece()
                                    self._can_en_passant = False
                                    # checking if a pawn has made itself vulnerable to en-passant by double jumping
                                    if selected_piece.is_pawn:
                                        if selected_piece.is_first_move:
                                            if selected_piece.get_player().is_opposite:
                                                if clicked_square[
                                                    0] == 3:  # if the user chose to do a double pawn advance
                                                    self._can_en_passant = (clicked_square[0] - 1, clicked_square[1])
                                                else:
                                                    self._can_en_passant = False
                                            else:
                                                if clicked_square[0] == 4:
                                                    self._can_en_passant = (clicked_square[0] + 1, clicked_square[1])
                                                else:
                                                    self._can_en_passant = False
                                        else:
                                            self._can_en_passant = False
                                    else:
                                        self._can_en_passant = False

                                    self.current_player.move_piece(selected_piece, clicked_square)
                                    self.board.draw_board()
                                    self.board.update_squares(whole=True)
                                    # handle promotion of pawn
                                    if selected_piece.is_pawn:
                                        if selected_piece.can_be_promoted():
                                            self.promotion(selected_piece)
                                    self.board.draw_board()
                                    self.board.update_squares(whole=True)
                                    self.board.moves_displayed = False
                                    self.board.set_selected_piece(None)
                                    self.half_moves += 1
                                    self.current_player.is_turn = False
                                    # next player's turn
                                    self.current_player = self.playerW if self.current_player == self.playerB else self.playerB
                                    self.current_player.is_turn = True
                                    self.draw_player_label()
                                    self._end_of_turn()  # add fen to fen stack and display check checkmate and stalemate labels appropriately

                            # if user clicked on one of their pieces
                            if piece != 0 and not piece.is_dead and piece.get_color() == self.current_player.get_color():
                                if self.board.get_castling_mode():
                                    self.board.set_castling_mode(False)
                                    self.board.moves_displayed = False
                                    self.board.draw_board()
                                    self.board.update_squares(whole=True)
                                # if click the already selected piece again: remove the green squares and deselect the piece
                                if piece.is_selected:
                                    self.current_player.deselect_piece(piece)
                                # if there is a piece selected and the user clicks on another of their pieces or if it is the first click
                                else:
                                    if self.board.get_selected_piece() is not None:  # if it is not the first piece
                                        self.current_player.deselect_piece(self.board.get_selected_piece())
                                    # en_passant
                                    has_en_pass = False  # indicates whether the user has done en-passant capture
                                    if self._can_en_passant != False:
                                        selected_piece_pos = piece.get_pos()
                                        if self.current_player.is_opposite:
                                            # possible squares en_passant capture could occur from the selected pawn
                                            possible_en_pas_squares = [
                                                (selected_piece_pos[0] + 1, selected_piece_pos[1] - 1),
                                                (selected_piece_pos[0] + 1, selected_piece_pos[1] + 1)]
                                        else:
                                            possible_en_pas_squares = [
                                                (selected_piece_pos[0] - 1, selected_piece_pos[1] - 1),
                                                (selected_piece_pos[0] - 1, selected_piece_pos[1] + 1)]
                                        if self._can_en_passant in possible_en_pas_squares:  # check if the selected piece can en-passant capture
                                            '''check if the king is not under attack if en_passant is performed by 
                                               setting the board to how it will look if en_passant is performed
                                            '''
                                            current_fen = self.get_fen()  # save it to return back to the state
                                            self.board.set_piece(self._can_en_passant[0], self._can_en_passant[1],
                                                                 piece)
                                            self.board.set_piece(selected_piece_pos[0], selected_piece_pos[1], 0)

                                            # check that in this board configuration, the king is not in check
                                            if not self.board.is_under_attack(self.current_player.get_color(),
                                                                              [self.current_player.king_pos]):
                                                # return the board to the original state
                                                self.load_from_fen(current_fen)
                                                #
                                                self.board.draw_board()
                                                self.board.draw_green_squares([
                                                    self._can_en_passant])  # show a green square where the en -passant capture would occur
                                                self.board.update_squares(whole=True)
                                                if self.show_en_passant():  # if the user chooses to do en-passant when prompted
                                                    self.en_passant(piece)
                                                    self.current_player.deselect_piece(selected_piece)
                                                    has_en_pass = True
                                                    self._can_en_passant = False
                                                    self.board.draw_board()
                                                    pygame.display.update()
                                                    self.board.moves_displayed = False
                                                    self.board.set_selected_piece(None)
                                                    self.half_moves += 1
                                                    self.current_player.is_turn = False
                                                    # next player's turn
                                                    self.current_player = self.playerW if self.current_player == self.playerB else self.playerB
                                                    self.current_player.is_turn = True
                                                    self.draw_player_label()
                                                    self._end_of_turn()  # add to fen stack and display check checkmate and stalemate labels appropriately

                                            else:  # en passant not possible because it leaves teh king in check
                                                # return board to original state
                                                self.load_from_fen(current_fen)
                                                # show the normal valid moves
                                                self.board.draw_board()
                                        else:  # en passant not possible
                                            # show the normal valid moves
                                            self.board.draw_board()

                                    if has_en_pass == False:
                                        self.board.draw_board()
                                        pygame.display.update()
                                        self.current_player.select_piece(piece)

                            self.board.update_squares(whole=True)
                        self.board.update_squares()
                # if the user clicks the cross top right
                elif event.type == pygame.QUIT:
                    self.quit_game = True
                    self.quit()

    def quit(self):
        pygame.quit()
        quit()

    def draw_player_label(self):  # draws the "White" or "Black" label depending on who's turn it is
        self.white_label.erase(self.game_display)
        if self.current_player.get_color() == "W":
            self.white_label.draw(self.game_display)
            self.white_label.update()
        else:
            self.black_label.draw(self.game_display)
            self.black_label.update()

    def erase_widgets(self, widget_list):  # pass a list of Label or Button objects and it will erase them
        for widget in widget_list:
            widget.erase(self.game_display)

    def promotion(self, piece):  # display options for promotion with buttons to choose

        label1 = Label("Select type:", green, 520, 22, 30)
        q_btn = Button(550, 70, 100, 36, magenta, "Queen", green, font_size=27)
        kn_btn = Button(550, 109, 100, 36, magenta, "Knight", green, font_size=27)
        r_btn = Button(550, 148, 100, 36, magenta, "Rook", green, font_size=27)
        b_btn = Button(550, 187, 100, 36, magenta, "Bishop", green, font_size=27)
        label1.draw(self.game_display)
        label1.update()
        q_btn.draw(self.game_display)
        q_btn.update()
        kn_btn.draw(self.game_display)
        kn_btn.update()
        r_btn.draw(self.game_display)
        r_btn.update()
        b_btn.draw(self.game_display)
        b_btn.update()
        promotion_mode = True
        while promotion_mode:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if q_btn.is_over(mouse_pos):
                        promotion_mode = False
                        # promoting to queen
                        self._promote(piece, "Q")
                        self.erase_widgets([label1, q_btn, kn_btn, r_btn, b_btn])
                        return "Q"

                    if kn_btn.is_over(mouse_pos):
                        promotion_mode = False
                        # promoting to knight
                        self._promote(piece, "N")
                        self.erase_widgets([label1, q_btn, kn_btn, r_btn, b_btn])
                        return "N"
                    if r_btn.is_over(mouse_pos):
                        promotion_mode = False
                        # promoting to knight
                        self._promote(piece, "R")
                        self.erase_widgets([label1, q_btn, kn_btn, r_btn, b_btn])
                        return "R"
                    if b_btn.is_over(mouse_pos):
                        promotion_mode = False
                        # promoting to knight
                        self._promote(piece, "B")
                        self.erase_widgets([label1, q_btn, kn_btn, r_btn, b_btn])
                        return "B"
                if event.type == pygame.QUIT:
                    exit = True
                    self.quit()

    def _promote(self, piece, promote_to):
        self.board.push_move(f'P,{piece.get_pos()[0]}{piece.get_pos()[1]},{promote_to}')

    def undo(self):  # undoes the last half move
        if len(self.fen_stack) == 1:
            self.load_from_fen(self.fen_stack[0])

        elif len(self.fen_stack) == 2:
            self.fen_stack.pop()
            self.load_from_fen(self.fen_stack[0])
        else:
            self.fen_stack.pop()
            self.load_from_fen(self.fen_stack[-1])


class HumanVsAI(HumanVsHumanGame):
    def __init__(self, human_player, AI_player, board, game_display):
        if human_player.get_color() == "W":
            super().__init__(human_player, AI_player, board, game_display)
        else:
            super().__init__(AI_player, human_player, board, game_display)
        self.human_player = human_player
        # whenever the user plays against the AI, no matter the colour they choose, they will be at the close end of the board
        self.human_player.is_opposite = False
        self.AI_player = AI_player
        self.AI_player.is_opposite = True

    def get_AI_player(self):
        return self.AI_player

    def get_human_player(self):
        return self.human_player

    def game_over(self):  # if stalemate or draw occurs for the AI, game is done
        exit = False
        while not exit:
            for event in pygame.event.get():
                # if the user clicks the cross top right
                if event.type == pygame.QUIT:
                    exit = True
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.to_menu_btn.is_over(mouse_pos):
                        exit = True
                        self.go_to_main()

    # Main game loop for the AIvsHuman game. Modified from the HUmanVsHumanGame one
    def start(self):
        self.board.create_board(self.human_player, self.AI_player)
        self.board.draw_board()
        self.draw_player_label()
        self.castle_btn.draw(self.game_display)
        self.undo_btn.draw(self.game_display)
        self.AI_tip_btn.draw(self.game_display)
        self.to_menu_btn.draw(self.game_display)
        pygame.display.update()
        game_over = False

        while not self.quit_game and not game_over:
            if self.current_player.get_color() == self.AI_player.get_color():
                self._can_en_passant = False
                # AI move here
                if self.AI_player.is_stockfish:
                    self.AI_player.next_move(self.get_fen())
                else:
                    # my AI requires the game object
                    self.AI_player.next_move(self)

                self.board.draw_board()
                self.board.update_squares(whole=True)
                self.half_moves += 1
                self.current_player.is_turn = False
                self.current_player = self.human_player
                self.current_player.is_turn = True
                self.draw_player_label()
                self._end_of_turn()  # add to fen stack and display check checkmate and stalemate labels appropriately

            else:
                for event in pygame.event.get():
                    # Handling mouse clicks and position
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.undo_btn.is_over(mouse_pos) and self.half_moves >= 1:
                            self.undo()
                            self.undo()  # undo 2 times because if undone once ,it will be AI's turn
                            self.board.draw_board()
                            self.checkmate_label.erase(self.game_display)
                            self.draw_player_label()
                            self.board.update_squares(whole=True)

                        elif self.to_menu_btn.is_over(mouse_pos):
                            self.go_to_main()
                            break

                        # castling button
                        elif self.castle_btn.is_over(mouse_pos):
                            if self.board.get_castling_mode():  # if the buttons has been pressed before
                                self.board.set_castling_mode(False)
                                self.board.set_selected_piece(None)
                                self.board.draw_board()
                            else:
                                squares = self.board.draw_castling_squares(self.current_player)
                            self.board.update_squares(squares)
                        elif self.AI_tip_btn.is_over(mouse_pos):
                            self.show_best_move()
                        else:
                            # (row, col) of the clicked square
                            clicked_square = self.board.get_square(mouse_pos[0], mouse_pos[1])
                            if self.board.get_castling_mode() and clicked_square in squares:
                                king_pos = self.current_player.king_pos
                                # perform castling
                                if clicked_square[1] < 4:
                                    if self.current_player.is_opposite:
                                        if self.current_player.get_color() == "W":
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                        else:
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")
                                    else:
                                        if self.current_player.get_color() == "W":
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")
                                        else:
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                else:
                                    if self.current_player.is_opposite:
                                        if self.current_player.get_color() == "W":
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")
                                        else:
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                    else:
                                        if self.current_player.get_color() == "W":
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},K")
                                        else:
                                            self.board.push_move(f"C,{king_pos[0]}{king_pos[1]},Q")

                                self.board.update_squares(whole=True)
                                self.half_moves += 1
                                self.current_player.is_turn = False
                                self.current_player = self.AI_player
                                self.current_player.is_turn = True
                                self.draw_player_label()
                                self._end_of_turn()  # add fen to fen stack and display check checkmate and stalemate labels appropriately

                            elif clicked_square is not None:
                                piece = self.board.get_piece(clicked_square[0], clicked_square[1])
                                # moving pieces
                                if self.board.moves_displayed:
                                    valid_moves = self.board.get_selected_piece().get_valid_moves()
                                    if clicked_square in valid_moves:
                                        selected_piece = self.board.get_selected_piece()
                                        self._can_en_passant = False
                                        # en-passant capture
                                        # checking if a pawn has made itself vulnerable to en-passant by pawn advancing 2 squares
                                        if selected_piece.is_pawn:
                                            if selected_piece.is_first_move:
                                                if selected_piece.get_player().is_opposite:
                                                    if clicked_square[0] == 3:
                                                        self._can_en_passant = (
                                                            clicked_square[0] - 1, clicked_square[1])
                                                    else:
                                                        self._can_en_passant = False
                                                else:
                                                    if clicked_square[0] == 4:
                                                        self._can_en_passant = (
                                                            clicked_square[0] + 1, clicked_square[1])
                                                    else:
                                                        self._can_en_passant = False
                                            else:
                                                self._can_en_passant = False
                                        else:
                                            self._can_en_passant = False

                                        self.current_player.move_piece(selected_piece, clicked_square)
                                        self.board.draw_board()
                                        self.board.update_squares(whole=True)
                                        # handle promotion of pawn
                                        if selected_piece.is_pawn:
                                            if selected_piece.can_be_promoted():
                                                self.promotion(selected_piece)
                                        self.board.draw_board()
                                        self.board.update_squares(whole=True)
                                        self.board.moves_displayed = False
                                        self.board.set_selected_piece(None)
                                        self.half_moves += 1
                                        self.current_player.is_turn = False
                                        # next player's turn
                                        self.current_player = self.AI_player
                                        self.current_player.is_turn = True
                                        self.draw_player_label()
                                        self._end_of_turn()  # add fen to fen stack and display check checkmate and stalemate labels appropriately

                                # if user clicked on one of their pieces
                                if piece != 0 and not piece.is_dead and piece.get_color() == self.current_player.get_color():
                                    if self.board.get_castling_mode():
                                        self.board.set_castling_mode(False)
                                        self.board.moves_displayed = False
                                        self.board.draw_board()
                                        self.board.update_squares(whole=True)
                                    # if click the already selected piece again: remove the green squares and deselect the piece
                                    if piece.is_selected:
                                        self.current_player.deselect_piece(piece)
                                    # if there is a piece selected and the user clicks on another of their pieces or if it is the first click
                                    else:
                                        if self.board.get_selected_piece() is not None:  # if it is not the first piece
                                            self.current_player.deselect_piece(self.board.get_selected_piece())
                                        # en_passant
                                        has_en_pass = False  # indicates whether the user has done en-passant
                                        if self._can_en_passant != False:
                                            selected_piece_pos = piece.get_pos()
                                            if self.current_player.is_opposite:
                                                # possible squares en_passant capture could occur from the selected pawn
                                                possible_en_pas_squares = [
                                                    (selected_piece_pos[0] + 1, selected_piece_pos[1] - 1),
                                                    (selected_piece_pos[0] + 1, selected_piece_pos[1] + 1)]
                                            else:
                                                possible_en_pas_squares = [
                                                    (selected_piece_pos[0] - 1, selected_piece_pos[1] - 1),
                                                    (selected_piece_pos[0] - 1, selected_piece_pos[1] + 1)]
                                            if self._can_en_passant in possible_en_pas_squares:  # check if the selected piece can en-passant capture
                                                '''check if the king is not under attack if en_passant is performed by 
                                                   setting the board to how it will look if en_passant is performed
                                                '''
                                                current_fen = self.get_fen()  # save fen to return to it
                                                self.board.set_piece(self._can_en_passant[0],
                                                                     self._can_en_passant[1],
                                                                     piece)
                                                self.board.set_piece(selected_piece_pos[0], selected_piece_pos[1],
                                                                     0)

                                                # check that in this board configuration, the king is not in check
                                                if not self.board.is_under_attack(self.current_player.get_color(),
                                                                                  [
                                                                                      self.current_player.king_pos]):  # en_passant possible
                                                    # return the board to the original state
                                                    self.load_from_fen(current_fen)
                                                    #
                                                    self.board.draw_board()
                                                    self.board.draw_green_squares([
                                                        self._can_en_passant])  # show a green square where the en -passant capture would occur
                                                    self.board.update_squares(whole=True)
                                                    if self.show_en_passant():  # if the user chooses to do en-passant when prompted
                                                        self.en_passant(piece)
                                                        self.current_player.deselect_piece(selected_piece)
                                                        has_en_pass = True
                                                        self._can_en_passant = False
                                                        self.board.draw_board()
                                                        pygame.display.update()
                                                        self.board.moves_displayed = False
                                                        self.board.set_selected_piece(None)
                                                        self.half_moves += 1
                                                        self.current_player.is_turn = False
                                                        # next player's turn
                                                        self.current_player = self.playerW if self.current_player == self.playerB else self.playerB
                                                        self.current_player.is_turn = True
                                                        self.draw_player_label()
                                                        self._end_of_turn()  # add to fen stack and display check checkmate and stalemate labels appropriately

                                                else:  # en passant leaves king in check so not possible
                                                    # return board to original state
                                                    self.load_from_fen(current_fen)
                                                    # show the normal valid moves
                                                    self.board.draw_board()
                                            else:  # en passant not possible
                                                # show the normal valid moves
                                                self.board.draw_board()

                                        if has_en_pass == False:
                                            self.board.draw_board()
                                            pygame.display.update()
                                            self.current_player.select_piece(piece)

                                self.board.update_squares(whole=True)
                            self.board.update_squares()
                    # if the user clicks the cross top right
                    elif event.type == pygame.QUIT:
                        self.quit_game = True
                        self.quit()


class AIvsAI(HumanVsHumanGame):
    def __init__(self, playerW, playerB, board, game_display):
        super().__init__(playerW, playerB, board, game_display)

    def game_over(self):  # if stalemate or draw occurs for the AI so game is done
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    self.quit()

    def start(self):
        self.board.create_board(self.playerW, self.playerB)
        self.board.draw_board()
        self.draw_player_label()
        pygame.display.update()
        game_over = False

        while not self.quit_game and not game_over:
            opponent_player = self.playerB if self.current_player.get_color == "W" else self.playerW
            if not game_over:
                # self.draw_player_label()
                if self.current_player.is_stockfish:
                    self.current_player.next_move(self.get_fen())
                else:
                    self.current_player.next_move(opponent_player)

                self.board.draw_board()
                pygame.display.update()
                self.half_moves += 1
                self.current_player.is_turn = False
                self.current_player = self.playerW if self.current_player == self.playerB else self.playerB
                self.current_player.is_turn = True
                self.draw_player_label()
                if self.current_player.is_stalemate():
                    self.stalemate_label.draw(self.game_display)
                    self.stalemate_label.update()
                    game_over = True
                    self.game_over()
                    break
                elif self.check_draw() == True:
                    self.draw_label.draw(self.game_display)
                    self.draw_label.update()
                    game_over = True
                    self.game_over()
                    break
                elif self.current_player.is_in_checkmate():
                    self.checkmate_label.draw(self.game_display)
                    self.checkmate_label.update()
                    game_over = True
                    self.game_over()
                    break
                elif self.current_player.is_in_check():

                    self.check_label.draw(self.game_display)
                    self.check_label.update()
                else:
                    self.checkmate_label.erase(self.game_display)
            for event in pygame.event.get():
                # if the user clicks the cross top right
                if event.type == pygame.QUIT:
                    game_over = True
                    break


def menu(GAME_DISPLAY):
    # if the 1-Player option is chosen in the main menu
    def one_player_menu():
        one_player_title_label = Label("1-Player", magenta, 300, 125, 70, font)
        back_btn = Button(0, 0, 60, 30, blue, "Back", magenta, font, 23)

        # chosing difficulty:0,1,2
        def difficulty_menu():
            GAME_DISPLAY.fill(green)
            one_player_title_label.draw(GAME_DISPLAY)
            difficulty_label = Label("Select the difficulty of AI ", magenta, 210, 230, 35, font)
            difficulty_label.draw(GAME_DISPLAY)
            # drawing all the buttons to choose depth
            depth_buttons = []
            x = 180
            y = 300
            for i in range(1, 21):
                btn = Button(x, y, 40, 40, blue, str(i), magenta, font, 25)
                x += 50
                if x > 640:
                    x = 180
                    y += 50
                depth_buttons.append(btn)
                btn.draw(GAME_DISPLAY)
            back_btn.draw(GAME_DISPLAY)
            pygame.display.update()
            back = False
            done = False

            while not done and not back:
                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()

                        if back_btn.is_over(mouse_pos):
                            back = True
                        else:
                            for btn in depth_buttons:
                                if btn.is_over(mouse_pos):
                                    depth = int(btn.get_text())
                                    done = True

                    # if the user clicks the cross top right
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            if back:
                main_menu()
            else:
                return depth

        # 1 player colout menu
        def color_menu(diff):
            GAME_DISPLAY.fill(green)
            one_player_title_label.draw(GAME_DISPLAY)
            diff_label = Label(f"Difficulty: {str(diff)}", magenta, 347, 220, 26, font)
            diff_label.draw(GAME_DISPLAY)
            color_label = Label("Color", magenta, 365, 260, 35, font)
            color_label.draw(GAME_DISPLAY)
            w_btn = Button(283, 315, 110, 50, blue, "White", white, font, 35)
            w_btn.draw(GAME_DISPLAY)
            b_btn = Button(433, 315, 110, 50, blue, "Black", black, font, 35)
            b_btn.draw(GAME_DISPLAY)
            back_btn.draw(GAME_DISPLAY)
            pygame.display.update()
            back = False
            done = False
            while not done and not back:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if w_btn.is_over(mouse_pos):
                            color = "W"
                            done = True
                        elif b_btn.is_over(mouse_pos):
                            color = "B"
                            done = True
                        elif back_btn.is_over(mouse_pos):
                            back = True
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
            if back:
                one_player_menu()
            else:
                return color

        depth = difficulty_menu()
        c = color_menu(depth)
        return (c, depth)

    def main_menu():
        GAME_DISPLAY.fill(green)
        title_label = Label("CHESS v4.2.0", magenta, 190, 125, 70, font)
        two_player_btn = Button(173, 250, 200, 150, blue, "2-Player", magenta, font, 50)
        two_player_btn.draw(GAME_DISPLAY)
        one_player_btn = Button(453, 250, 200, 150, blue, "1-Player", magenta, font, 50)
        one_player_btn.draw(GAME_DISPLAY)
        title_label.draw(GAME_DISPLAY)
        pygame.display.update()
        end_menu = False
        while not end_menu:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if two_player_btn.is_over(mouse_pos):
                        # if the 2 player button is clicked in the menu
                        board = Board(GAME_DISPLAY)
                        GAME_DISPLAY.fill(black)
                        playerW = PlayerHuman("W", board, is_opposite=False)
                        playerB = PlayerHuman("B", board, True)
                        board.create_board(playerW, playerB)
                        game = HumanVsHumanGame(playerW, playerB, board, GAME_DISPLAY)
                        game.start()
                        end_menu = True
                    elif one_player_btn.is_over(mouse_pos):
                        # what happens if the one-player option is clicked
                        color, depth = one_player_menu()
                        board = Board(GAME_DISPLAY)
                        GAME_DISPLAY.fill(black)
                        human_player = PlayerHuman(color, board, is_opposite=False)
                        AI_color = "W" if color == "B" else "B"
                        if depth >= 4:
                            AI_player = PlayerStockfish(AI_color, board, depth - 3, True)
                        else:
                            AI_player = PlayerAI(AI_color, board, depth, True)
                        if color == "B":
                            board.create_board(AI_player, human_player)
                        else:
                            board.create_board(human_player, AI_player)

                        game = HumanVsAI(human_player, AI_player, board, GAME_DISPLAY)
                        game.start()
                        end_menu = True
                # if the user clicks the cross top right
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    main_menu()
