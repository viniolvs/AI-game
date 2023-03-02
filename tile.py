import pygame
from pygame.sprite import Sprite


class Tile(Sprite):
    def __init__(self, screen, x, y, settings, image=""):
        super(Tile, self).__init__()
        self.screen = screen
        self.tile_size = settings.tile_size
        if image == "":
            self.image = pygame.Surface((self.tile_size, self.tile_size))
            self.image.fill(settings.bg_color)
        else:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale(
                self.image, (self.tile_size, self.tile_size)
            )

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.is_wall = False

    def setImage(self, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(
            self.image, (self.tile_size, self.tile_size)
        )

    def blitme(self):
        self.screen.blit(self.image, self.rect)
