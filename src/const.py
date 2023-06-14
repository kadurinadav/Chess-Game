
# Screen dimensions
WIDTH = 800
HEIGHT = 800

# Board dimensions
ROWS = 8
COLS = 8
SQSIZE = WIDTH // COLS

# Alphacols
COLS_LETTERS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h',}

# Pawn promotion selection
CHOSEN_PIECE = {0: "white_queen", 1: "white_rook", 2: "white_bishop", 3: "white_knight", 4: "black_knight", 5: "black_bishop", 6: "black_rook", 7:  "black_queen" }

# Piece symbols
PIECE_SYMBOLS = {"white_king": 'K', "white_queen": 'Q', "white_rook": 'R',"white_bishop": 'B', "white_knight": 'N', "white_pawn": 'P',
                 "black_king": 'k', "black_queen": 'q', "black_rook": 'r',"black_bishop": 'b', "black_knight": 'n', "black_pawn": 'p'}

# Casteling rights
"""                               castle   move   in      in
                                  right    map    binary  decimal

white king moved                   1111  &  0011 = 0011     3
white king's rook moved            1111  &  0111 = 0111     7
white queen's rook moved           1111  &  1011 = 1011     11
black king moved                   1111  &  1100 = 1100     3
black king's rook moved            1111  &  1110 = 1110     14
black queen's rook moved           1111  &  1101 = 1101    13
"""
CASTELING_RIGHTS = [14, 15, 15, 15, 12, 15, 15, 13,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    15, 15, 15, 15, 15, 15, 15, 15,
                    11, 15, 15, 15, 3, 15, 15, 7]
ENUM_CASTELING = {'K' : 8, 'Q' : 4, 'k' : 2, 'q' : 1}