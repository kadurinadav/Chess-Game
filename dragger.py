import pygame
from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX = 0
        self.mouseY = 0
        self.clicked_row = 0
        self.clicked_col = 0
        self.released_row = 0
        self.released_col = 0
    
    def update_blit(self, surface):
        """
            Update the piece image to move with the mouse
        """
        img = pygame.image.load(self.piece.image)
        img_center = (self.mouseX, self.mouseY)
        image_rect = img.get_rect(center = img_center)
        surface.blit(img, image_rect)

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos
    
    def save_initial_pos(self):
        """
            Save clicked square 
        """
        self.clicked_row = self.mouseY // SQSIZE
        self.clicked_col = self.mouseX // SQSIZE
    
    def save_final_pos(self):
        """
            Save released square
        """
        self.released_row = self.mouseY // SQSIZE
        self.released_col = self.mouseX // SQSIZE
    
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def undrag_piece(self):
        self.piece = None
        self.dragging = False

