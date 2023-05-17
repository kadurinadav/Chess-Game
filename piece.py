import os
from const import *

class Piece:

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.symbol = PIECE_SYMBOLS[f"{color}_{name}"]
        self.valid_moves = []
        self.has_moved = False
        self.image = os.path.join(f'assets/images/{self.color}_{self.name}.png')

    def __eq__(self, other):
        """
            Check if two pieces are equal
        """
        return self.name == other.name and self.color == other.color and self.valid_moves == other.valid_moves 
    
    def add_move(self, move):
        """
            Add the move to piece valid moves list
        """
        self.valid_moves.append(move)

    def clear_moves(self):
        """
            Clear piece valid moves list
        """
        self.valid_moves = []

class Pawn(Piece):
    
    def __init__(self, color):
        self.direction = -1 if color == 'white' else 1
        self.en_passant = False
        super().__init__('pawn', color)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color)

class King(Piece):

    def __init__(self, color):
        super().__init__('king', color)