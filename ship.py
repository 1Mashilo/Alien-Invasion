
import pygame
from pygame.sprite import Sprite
import os

class Ship(Sprite):
    '''A class to manage the ship'''

    def __init__(self, ai_game):
        '''Initialize the ship and set its starting position.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        self.moving_right = False
        self.moving_left = False

        image_path = os.path.join(os.path.dirname(__file__), 'ship.bmp')
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_speed

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    
    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)