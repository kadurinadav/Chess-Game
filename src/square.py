
class Square:
    
    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        """
            Check if two squares are equal
        """
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        """
            Check if square has piece on it
        """
        return self.piece is not None
    
    def is_empty(self):
        """
            Check if square is empty
        """
        return not self.has_piece()
    
    def has_team_piece(self, color):
        """
            Check if square has team piece on it
        """
        return self.has_piece() and self.piece.color == color
     
    def has_rival_piece(self, color):
        """
            Check if square has rival piece on it
        """
        return self.has_piece() and self.piece.color != color
    
    def is_empty_or_rival(self, color):
        """
            Check if square is empty or has rival piece on it
        """
        return self.is_empty() or self.has_rival_piece(color)

    @staticmethod
    def in_range(*args):
        """
            Check if square is in the range of the board
        """
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True