
import pygame

class ShipLives:
    def __init__(self, ai_game, ship_image, ship_rect): 
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = ship_image
        self.rect = ship_rect
        self.rect.x = 10  
        self.rect.y = 10 

    def draw_lives(self, lives):
        for i in range(lives):
            self.screen.blit(self.image, (self.rect.x + i * (self.rect.width + 5), self.rect.y))
