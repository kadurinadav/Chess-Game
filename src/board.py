from src.const import *
from src.piece import *
from src.square import Square
from src.move import Move
from src.sound import Sound
import copy

class Board:

    def __init__(self):
        # Create 8*8 chess board
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for row in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
        # Add white and black pieces
        self._add_piece('white')
        self._add_piece('black')
        # save player turn
        self.next_player = 'white'
        # Save last move in the game
        self.last_move = None
        # save if last move was pawn promotion move
        self.pawn_promotion = False
        # save castle and en passant rights
        self.casteling_rights = 15 # 1111 in binary
        self.en_passant_rights = '-'
        # create board history hash map
        self.board_history = {}
        self.add_board_to_history()

    def _add_piece(self, color):
        """
            Initiallize all pieces at the beggining of the game
        """
        pawn_row, other_row = (6, 7) if color == 'white' else (1, 0)
        
        # Pawns
        for col in range(COLS):
           self.squares[pawn_row][col] = Square(pawn_row, col, Pawn(color)) 
        # Knights
        self.squares[other_row][1] = Square(other_row, 1, Knight(color))
        self.squares[other_row][6] = Square(other_row, 6, Knight(color))
        # Bishops
        self.squares[other_row][2] = Square(other_row, 2, Bishop(color))
        self.squares[other_row][5] = Square(other_row, 5, Bishop(color))
        # Rooks
        self.squares[other_row][0] = Square(other_row, 0, Rook(color))
        self.squares[other_row][7] = Square(other_row, 7, Rook(color))
        # Queen
        self.squares[other_row][3] = Square(other_row, 3, Queen(color))
        # King
        self.squares[other_row][4] = Square(other_row, 4, King(color))   

    def next_turn(self):
        """
            Update next player turn
        """
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def valid_move(self, piece, move):
        """
            Check if move is in piece valid moves
        """
        return move in piece.valid_moves

    def calc_moves(self, piece, row, col, check_flag):
        """
            Calculate all possible moves of a specific piece on specific position
        """

        def create_move(possible_move_row, possible_move_col, casteling = None):
            """
                Create new move and before adding it to piece valid moves list, the fucntion checks if the move is valid using in_check function:
                1. Not in check after this move
                2. Not castle if my king is in check or passing through a check while he castle
            """
            # create new move
            initial_sq = Square(row, col)
            final_sq = Square(possible_move_row, possible_move_col, piece)
            move = Move(initial_sq, final_sq)

            # check potential checks
            if check_flag:
                # if not casteling move
                if not casteling:
                    # check if after this move my king is in check. if in_check return true that means this move is not valid and we will not add it to piece.valid_moves.
                    if not self.in_check(piece, move):  
                        # add new move to valid moves list
                        piece.add_move(move)
                # casteling move
                else:
                    if casteling == "king_casteling":
                        # create additinal 2 moves in order to check that the king is not in check and he is not entering a check while he castle
                        final_sq2 = Square(possible_move_row, possible_move_col-1)
                        final_sq3 = Square(possible_move_row, possible_move_col-2)
                        move_2 = Move(initial_sq, final_sq2)
                        move_3 = Move(initial_sq, final_sq3)
                        if not self.in_check(piece, move) and not self.in_check(piece, move_2) and not self.in_check(piece, move_3):
                            # add new move to valid moves list
                            piece.add_move(move)
                    elif casteling == "queen_casteling":
                        # create additinal 3 moves in order to check that the king is not in check and he is not entering a check while he castle
                        final_sq2 = Square(possible_move_row, possible_move_col+1)
                        final_sq3 = Square(possible_move_row, possible_move_col+2)
                        final_sq4 = Square(possible_move_row, possible_move_col+3)
                        move_2 = Move(initial_sq, final_sq2)
                        move_3 = Move(initial_sq, final_sq3)
                        move_4 = Move(initial_sq, final_sq4)
                        if not self.in_check(piece, move) and not self.in_check(piece, move_2) and not self.in_check(piece, move_3) \
                        and not self.in_check(piece, move_4):
                            # add new move to valid moves list
                            piece.add_move(move)
            # we will enter this else just if calc_moves was called inside in_check function. That is, the adding of the move is part of a test in order to check if after this move our king is in check
            else:
                # add new move to valid moves list
                piece.add_move(move)
        
        def pawn_moves():
            """
                calculate all possible moves of a pawn - vertical, diagonal and en passant moves
            """
            # vertical moves
            steps = 1 if piece.has_moved else 2
            start = row + piece.direction
            end = row + (piece.direction * (steps + 1))
            for possible_move_row in range(start, end, piece.direction):
                # check if square in range
                if Square.in_range(possible_move_row):
                    # check if square is empty
                    if self.squares[possible_move_row][col].is_empty():
                        create_move(possible_move_row, col)
                    # blocked by rival piece
                    else: break
                # square not in range
                else: break

            # diagonal moves
            possible_move_row = row + piece.direction
            possible_move_cols = [col+1, col-1]
            for possible_move_col in possible_move_cols:
                # check if square in range
                if Square.in_range(possible_move_row, possible_move_col):
                    # check if square has rival piece on it
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        create_move(possible_move_row, possible_move_col)
                         
            # en paasant move
            if piece.color == "black" and row == 4 or piece.color == "white" and row == 3:
                possible_move_cols = [col+1, col-1]
                for possible_move_col in possible_move_cols:
                    # check if square in range
                    if Square.in_range(row, possible_move_col):
                        # check if square has rival piece on it
                        if self.squares[row][possible_move_col].has_rival_piece(piece.color):
                            rival_piece = self.squares[row][possible_move_col].piece
                            # check if rival piece is a pawn and en_passant property is set to True
                            if isinstance(rival_piece, Pawn) and rival_piece.en_passant:
                                create_move(possible_move_row, possible_move_col)

        def knight_moves():
            """
                calculate all possible moves of a knight
            """
            # 8 possible moves
            possible_moves = [
                (row-2, col+1), # 2 rows up 1 column right
                (row-2, col-1), # 2 rows up 1 column left
                (row+2, col+1), # 2 rows down 1 column right
                (row+2, col-1), # 2 rows down 1 column left
                (row-1, col+2), # 1 row up 2 columns right
                (row-1, col-2), # 1 row up 2 columns left
                (row+1, col+2), # 1 row down 2 columns right
                (row+1, col-2)  # 1 row down 2 columns left 
            ]

            # loop all 8 possible moves
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                # check if square in range
                if Square.in_range(possible_move_row, possible_move_col):
                    # check if square is empty or has rival piece on it
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        create_move(possible_move_row, possible_move_col)

        def straightline_moves(incrs):
            """
                calculate all possible moves of a bishop, rook or queen depends on incrs
            """
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    # check if square in range
                    if Square.in_range(possible_move_row, possible_move_col):
                        # check if empty
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            # create move and continue to next iteration
                            create_move(possible_move_row, possible_move_col)
                        # check if rival piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # create move and break because the rival piece is blocking us from advance
                            create_move(possible_move_row, possible_move_col)
                            break
                        # check if team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            # break, we can't move to a team piece square
                            break
                    # not in range
                    else: break

                    # advance possible_move_row by row_incr and possible_move_col by col_incr
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            """
                calculate all possible moves of a king - standart move or casteling move
            """
            # 8 possible moves
            possible_moves = [
                (row-1, col),   # up
                (row-1, col-1), # up-left
                (row-1, col+1), # up-right
                (row, col-1),   # left
                (row, col+1),   # right
                (row+1, col),   # down
                (row+1, col-1), # down-left
                (row+1, col+1)  # down-right
            ]   
            
            # loop all 8 possible moves
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                # check if square in range
                if Square.in_range(possible_move_row, possible_move_col):
                    # check if square is empty or has rival piece on it
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        create_move(possible_move_row, possible_move_col)

            # castelling moves
            if not piece.has_moved:
                # check if king casteling is possible
                if self.squares[row][col+1].is_empty() and self.squares[row][col+2].is_empty() \
                and isinstance(self.squares[row][col+3].piece, Rook) and not self.squares[row][col+3].piece.has_moved:
                    create_move(row, col+2, casteling = 'king_casteling')
                # check if queen casteling is possible
                elif self.squares[row][col-1].is_empty() and self.squares[row][col-2].is_empty() and self.squares[row][col-3].is_empty() \
                and isinstance(self.squares[row][col-4].piece, Rook) and not self.squares[row][col-4].piece.has_moved:
                    create_move(row, col-3, casteling = 'queen_casteling')

        # clear all previous valid_moves
        piece.clear_moves()

        if isinstance(piece, Pawn): 
            pawn_moves()
        elif isinstance(piece, Knight): 
            knight_moves()
        elif isinstance(piece, Bishop): 
            straightline_moves(
                [
                    (-1, 1), # up-right
                    (-1, -1), # up-left
                    (1, 1), # down-right
                    (1, -1) # down-left
                ])
        elif isinstance(piece, Rook): 
            straightline_moves(
                [
                    (-1, 0), # up
                    (1, 0), # down
                    (0, 1), # right
                    (0, -1) # left
                ])
        elif isinstance(piece, Queen): 
            straightline_moves(
                [
                    (-1, 1), # up-right
                    (-1, -1), # up-left
                    (1, 1), # down-right
                    (1, -1), # down-left
                    (-1, 0), # up
                    (1, 0), # down
                    (0, 1), # right
                    (0, -1) # left
                ])
        elif isinstance(piece, King): 
            king_moves()
          
    def in_check(self, piece, move = None):
        """
            creating temporary board and temporary piece and simulating the possible move on the board. Then, we check if after moving the piece from initial square to final square my king is in check by a rival piece
        """
        # create temporary deepcopy of our board and piece
        tmp_board = copy.deepcopy(self)
        tmp_piece = copy.deepcopy(piece)
        # move the piece on the temporary board
        tmp_board.move(tmp_piece, move, simulating = True) 
        # loop all squares on board and check if there is check 
        for row in range(ROWS):
            for col in range(COLS):
                sq = tmp_board.squares[row][col]
                if sq.has_rival_piece(piece.color):
                    rival_piece = tmp_board.squares[sq.row][sq.col].piece
                    tmp_board.calc_moves(rival_piece, row, col, check_flag = False)
                    for possible_move in rival_piece.valid_moves:
                        final_sq = possible_move.final_sq
                        possible_move_row, possible_move_col = final_sq.row, final_sq.col
                        p = tmp_board.squares[possible_move_row][possible_move_col].piece
                        if isinstance(p, King):
                            return True
        return False
                
    def move(self, piece, move, simulating = False):
        """
            move the piece from initial square to final square
        """
        initial_row, initial_col = move.initial_sq.row, move.initial_sq.col
        final_row, final_col = move.final_sq.row , move.final_sq.col
        final_sq_is_empty = self.squares[final_row][final_col].is_empty()
        # console board move update
        self.squares[initial_row][initial_col].piece = None
        self.squares[final_row][final_col].piece = piece
        
        if not simulating:
            self.update_en_passant_rights('-')  
            if isinstance(piece, Pawn):
                # update en_passant property and en_passant_rights if pawn move 2 squares from start position             
                if final_row == initial_row + (2 * piece.direction):
                    piece.en_passant = True
                    self.update_en_passant_rights(COLS_LETTERS[final_col] + str(final_row-1)) 
                # check if this move is en_passant - if yes capture the rival pawn
                elif initial_col != final_col and final_sq_is_empty:
                    self.en_passant_capture(initial_row, final_col)
                # clear board history if it is pawn move
                self.clear_board_history()
                    
            if isinstance(piece, King):
                # check if king casteling move
                if initial_col == 4 and final_col == 6:
                    self.king_casteling(final_row)
                # check if queen casteling move
                elif initial_col == 4 and final_col == 1:
                    self.queen_casteling(final_row)
            
            # update last move
            self.last_move = move
            # mark the piece as moved
            piece.has_moved = True
            # clear valid_moves list
            piece.clear_moves()
            # update casteling rights
            self.update_casteling_rights(move)
                   
    def is_stalemate_or_checkmate(self, next_player): 
        """
            check if checkmate or stalemate        
        """
        # check if next_player has a valid move to play
        for row in range(ROWS):
            for col in range(COLS):
                # check if square has next_player piece on it
                if self.squares[row][col].has_team_piece(next_player):
                    team_piece = self.squares[row][col].piece
                    self.calc_moves(team_piece, row, col, check_flag = True)
                    if len(team_piece.valid_moves) != 0:
                        return 0
                    
        # if we reached here there is no valid move to play. Now, we check if it is checkmate or stalmate by checking if next_player king is in check or not
        for row in range(ROWS):
            for col in range(COLS):
                # check if square has next_player piece on it
                if self.squares[row][col].has_team_piece(next_player):
                    team_piece = self.squares[row][col].piece
                    if isinstance(team_piece, King):
                        # create new move
                        initial_sq = Square(row, col)
                        final_sq = Square(row, col, team_piece)
                        move = Move(initial_sq, final_sq)   
                        if self.in_check(team_piece, move):  
                            return 1 # checkmate
        return 2 # stalemate
      
    # pawn promotion functions 
    def check_if_pawn_promotion_move(self, final_sq):
        """
            check if it is pawn promotion move
        """   
        return True if final_sq.row == 0 or final_sq.row == 7 else False
    
    def choose_pawn_promotion_piece(self, clicked_row, clicked_col): 
        """
            Promote the pawn to the piece chosen by the player
        """
        # set row and col of the pawn that should be promoted
        row = self.last_move.final_sq.row
        col = self.last_move.final_sq.col
        # set piece color
        color = "white" if row == 0 else "black"
        row_condition = clicked_row >= 0 and clicked_row <= 3 if color == "white" else clicked_row >= 4 and clicked_row <= 7
        # check if cilcked on 1 out of 4 option squares depending on which color the pawn is
        if clicked_col == col and row_condition:
            # find chosen piece
            chosen_piece = CHOSEN_PIECE[clicked_row]
            # promote the pawn to the chosen piece
            if chosen_piece == f"{color}_queen":
                self.squares[row][col] = Square(row, col, Queen(color))
            elif chosen_piece == f"{color}_rook":
                self.squares[row][col] = Square(row, col, Rook(color))
            elif chosen_piece == f"{color}_bishop":
                self.squares[row][col] = Square(row, col, Bishop(color))
            elif chosen_piece == f"{color}_knight":
                self.squares[row][col] = Square(row, col, Knight(color))
            self.pawn_promotion = False
    
     # en passant functions
    
    # en passant functions
    def en_passant_capture(self, initial_row, final_col):
        """
            check if it is en passant move
        """
        # capture the rival pawn
        self.squares[initial_row][final_col].piece = None
        sound = Sound()
        sound.play_capture_sound()

    def set_false_en_passant(self):
        """
            set to false en passant property to all pawn other than last move piece
        """
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    tmp_piece = self.squares[row][col].piece
                    if isinstance(tmp_piece, Pawn):
                        if self.last_move:
                            if self.last_move.final_sq.piece != tmp_piece:
                                tmp_piece.en_passant = False

    # casteling functions
    def king_casteling(self, final_row):
        """
            king casteling move - update rook position to the left of the king
        """
        self.squares[final_row][5].piece = self.squares[final_row][7].piece
        self.squares[final_row][7].piece = None

    def queen_casteling(self, final_row):
        """
            queen casteling move - update rook position to the right of the king
        """
        self.squares[final_row][2].piece = self.squares[final_row][0].piece
        self.squares[final_row][0].piece = None

    # threefold repetition functions
    def check_threefold_repetition(self):
        """
            check if the game reaches the same position three times - if so, a draw is declared
        """
        for v in self.board_history.values():
            if v == 3:
                return True
        return False

    def board_to_FEN(self):
        """
            converts board table to Forsyth - Edwards Notation
        """
        fen = ""
        for row in range(ROWS):
            empty = 0
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    if empty > 0:
                        fen += str(empty)
                        empty = 0
                    fen += self.squares[row][col].piece.symbol
                else:
                    empty += 1
            if empty > 0:
                fen += str(empty)
            if col < COLS-1: # Added to eliminate last '/'
                fen += '/'
        
        active_color = 'w' if self.next_player == 'white' else 'b'
        casteling_rights = self.binary_to_str_casteling_rights()
        fen += " " + active_color + " " + casteling_rights + " " + self.en_passant_rights

        return fen
    
    def add_board_to_history(self):
        """
            add board to history hashmap. if board is already in the hashmap, increment his value by 1
        """
        # create fen string from board
        fen = self.board_to_FEN()
        # add it to history board hashmap if not exist, else increment board_history[fen] by one
        self.board_history[fen] = self.board_history[fen] + 1 if fen in self.board_history else 1

    def clear_board_history(self):
        """
            clear board history hashmap
        """
        self.board_history = {}
    
    def update_en_passant_rights(self, str):
        self.en_passant_rights = str

    def update_casteling_rights(self, move):
        initial_row, initial_col = move.initial_sq.row, move.initial_sq.col
        final_row, final_col = move.final_sq.row , move.final_sq.col
        # save curr casteling rights
        curr_casteling_rights = self.casteling_rights
        # bitwise & casteling_rights with CASTELING_RIGHTS[initial_sq] and CASTELING_RIGHTS[final_sq] in order to update castelling right
        self.casteling_rights &= CASTELING_RIGHTS[(8 * initial_row) + initial_col]
        self.casteling_rights &= CASTELING_RIGHTS[(8 * final_row) + final_col]
        # if casteling rights have changed, then clear board history
        if curr_casteling_rights != self.casteling_rights:
            self.clear_board_history()
        
    def binary_to_str_casteling_rights(self):
        """
            Convert binary representation to fen representation - ex. 1101 to 'KQ-q'
        """
        white_king_casteling = 'K' if self.casteling_rights & ENUM_CASTELING['K'] else '-'
        white_queen_casteling = 'Q' if self.casteling_rights & ENUM_CASTELING['Q'] else '-'
        black_king_casteling = 'k' if self.casteling_rights & ENUM_CASTELING['k'] else '-'
        black_queen_casteling = 'q' if self.casteling_rights & ENUM_CASTELING['q'] else '-'
        
        return white_king_casteling + white_queen_casteling + black_king_casteling + black_queen_casteling  
               
    # insufficiant material functions
    def insufficient_material(self):
        """
            Checking whether both sides do not have enough pieces in order to win the game. if that's the case, a draw is declared
        """
        return self.insufficient_material_check("white") and self.insufficient_material_check("black")
    
    def insufficient_material_check(self, color):
        """
            Check if specific color have any one of the following, and there are no pawns on the board: 
            1. A lone king 
            2. A king and bishop
            3. A king and knight

            Return False if there are enough pieces to play, else return True
        """
        bishops_count = 0
        knights_count = 0
        # loop board
        for row in range(ROWS):
            for col in range(COLS):
                # check if team piece
                if self.squares[row][col].has_team_piece(color):
                    piece = self.squares[row][col].piece
                    # if there is pawn, queen or rook on the board then return False, which means there are still enough pieces
                    if isinstance(piece, Pawn) or isinstance(piece, Queen) or isinstance(piece, Rook):
                        return False
                    # if bishop
                    elif isinstance(piece, Bishop):
                        bishops_count += 1
                    # if knight
                    elif isinstance(piece, Knight):
                        bishops_count += 1 
        # no pawns, rooks or queen on board. return False only if there are - 2 bishops or 2 knights or 1 bishop and 1 knight on board
        if bishops_count == 2 or knights_count == 2 or (bishops_count == 1 and knights_count == 1):
            return False
        # insufficient material
        return True

                        
        
