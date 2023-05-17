import pygame
from board import Board
from dragger import Dragger
from sound import Sound
from piece import *
from const import *

class Game:

    def __init__(self):
        self.dragger = Dragger()
        self.board = Board()
        self.checkmate = False
        self.stalemate = False
        self.threefold_repetition = False
        self.insufficient_material = False

    # blit methods 

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                color = (234, 235, 200)  if (row + col) % 2 == 0 else (119, 154, 88)
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
                # row coordinates
                if col == 0:
                    font = pygame.font.SysFont('monospace', 18, bold = True)
                    color = '#BDB3B3' if (row + col) % 2 == 0 else '#F9F8F8'
                    label = font.render(str(ROWS-row), 1, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    surface.blit(label, label_pos)
                # col coordinates
                if row == 7:
                    font = pygame.font.SysFont('monospace', 18, bold = True)
                    color = '#BDB3B3' if (row + col) % 2 == 0 else '#F9F8F8'
                    label = font.render(COLS_LETTERS[col], 1, color)
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(label, label_pos)
  
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # check if square has a piece
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # if checkmate - paint the loosing king in red
                    if self.checkmate and isinstance(piece, King) and piece.color != self.board.last_move.final_sq.piece.color:
                        piece.image = os.path.join(f'assets/images/red_king.png')
                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.image)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        image_rect = img.get_rect(center = img_center)
                        surface.blit(img, image_rect)
    
    def show_valid_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop all valid moves
            for move in piece.valid_moves:
                row, col = move.final_sq.row, move.final_sq.col
                # check if square has rival piece on it - if yes we will circle it according to the square color it stands on
                if self.board.squares[row][col].has_rival_piece(move.final_sq.piece.color):
                    img_path = os.path.join(f'assets/images/capture_light_green_dot.png') if (row + col) % 2 == 0 else os.path.join(f'assets/images/capture_green_dot.png')
                # the square is empty - thus we will show only small circle according to the square color
                else:
                    img_path = os.path.join(f'assets/images/light_green_dot.png') if (row + col) % 2 == 0 else os.path.join(f'assets/images/green_dot.png')      
                # check if valid move is on yellow square - which mean last move squares
                last_move = self.board.last_move
                if last_move:
                    if (row == last_move.initial_sq.row and col == last_move.initial_sq.col) or (row == last_move.final_sq.row and col == last_move.final_sq.col):
                        # check if square has rival piece on it - if yes we will circle in yellow
                        if self.board.squares[row][col].has_rival_piece(move.final_sq.piece.color):
                            img_path = os.path.join(f'assets/images/capture_yellow_dot.png')
                        # the square is empty - thus we will show only small yellow circle
                        else:
                            img_path = os.path.join(f'assets/images/yellow_dot.png')       
                img = pygame.image.load(img_path)
                img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                image_rect = img.get_rect(center = img_center)
                surface.blit(img, image_rect)
    
    def show_last_move(self, surface):
        last_move = self.board.last_move
        if last_move:
            initial_sq, final_sq = last_move.initial_sq, last_move.final_sq
            for sq in [initial_sq, final_sq]:
                color = '#EEEE71'
                rect = sq.col * SQSIZE, sq.row * SQSIZE, SQSIZE, SQSIZE
                pygame.draw.rect(surface, color, rect)

    def show_pawn_promotion_selection(self, surface):
        # set row and col of the pawn that should be promoted
        row = self.board.last_move.final_sq.row
        col = self.board.last_move.final_sq.col
        # set piece color
        piece_color = "white" if row == 0 else "black"
        direction = 1 if piece_color == "white" else -1
        # loop 4 squares from buttom-up or top-down depends on pawn's color
        for tmp_row in range(row, row + (direction * 4), direction):
            # draw white rectangles
            color = (255, 255, 255)
            rect = (col * SQSIZE, tmp_row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect)
            # blit pieces image on the white rectangles
            img = pygame.image.load(os.path.join(f'assets/images/{CHOSEN_PIECE[tmp_row]}.png'))
            img_center = col * SQSIZE + SQSIZE // 2, tmp_row * SQSIZE + SQSIZE // 2
            image_rect = img.get_rect(center = img_center)
            surface.blit(img, image_rect)

    def show_message(self, surface, message):
            font = pygame.font.SysFont('monospace', 40, bold = True)
            text = font.render(message, True, (255, 255, 255), (243,58,58))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            surface.blit(text, text_rect)

    def show(self, surface):
        self.show_bg(surface)
        self.show_last_move(surface)
        self.show_valid_moves(surface)
        self.show_pieces(surface)
        if self.board.pawn_promotion:
            self.show_pawn_promotion_selection(surface)
        if self.checkmate:
            self.show_message(surface, "Checkmate")
        elif self.stalemate:
            self.show_message(surface, "Stalmate")
        elif self.threefold_repetition:
            self.show_message(surface, "Draw by Threefold Repetition")
        elif self.insufficient_material:
            self.show_message(surface, "Draw by Insufficiant Material")
        if self.dragger.dragging:
                self.dragger.update_blit(surface)
        
    # other methods

    def play_sound(self, captured = False):
        """
            play move or capture sound
        """
        sound = Sound()
        if captured:
            sound.play_capture_sound()
        else:
            sound.play_move_sound()

    def restart(self):
        """
            restart the game by press 'R' key on the keyboard
        """
        self.__init__()
            
