import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, settings, screen, player):
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(
                0, 0, settings.bullet_width, settings.bullet_height
                )
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.color = settings.bullet_color

        # Pos do projetil
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        # velocidade do projetil
        self.speed_factor = settings.bullet_speed_factor
        # direção do projetil
        self.direction = player.last_move

    # move o projetil na direção do último movimento do player
    def update(self):
        if self.direction == "right":
            self.x += self.speed_factor
            self.rect.x = self.x
        elif self.direction == "left":
            self.x -= self.speed_factor
            self.rect.x = self.x
        elif self.direction == "up":
            self.y -= self.speed_factor
            self.rect.y = self.y
        elif self.direction == "down":
            self.y += self.speed_factor
            self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
