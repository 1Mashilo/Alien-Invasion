import pygame
import random

class Star(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.size = random.randint(1, 3)
        self.color = (255, 255, 255) 

        self.image = pygame.Surface([self.size, self.size])
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_width)
        self.rect.y = random.randint(0, self.screen_height)