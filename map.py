import pygame


class Map:
    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load("images/map.png")
        self.image = pygame.transform.scale(self.image, screen.get_size())
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center

    def blitme(self):
        self.screen.blit(self.image, self.rect)
