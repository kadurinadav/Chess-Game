import pygame
import os

class Sound:

    def __init__(self):
        self.move_sound = pygame.mixer.Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = pygame.mixer.Sound(os.path.join('assets/sounds/capture.wav'))

    def play_move_sound(self):
        """
            play move sound
        """
        pygame.mixer.Sound.play(self.move_sound)

    def play_capture_sound(self):
        """
            play capture sound
        """
        pygame.mixer.Sound.play(self.capture_sound)