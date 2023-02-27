import pygame
import game_functions as gf
from collision import check_wall


class Player(object):
    """Inicializa a espaconave e define posicao inicial"""

    def __init__(self, settings, screen):
        self.screen = screen
        self.settings = settings
        # Carrega imagem e obtem rect
        self.image = pygame.image.load("images/player.bmp")
        self.image = pygame.transform.scale(self.image, settings.player_size)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.flipped = False  # Flag de imagem virada
        # Inicia cada nova espaconave na parte inferior central da tela
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.center = self.screen_rect.center

        # Valor decimal para centro do jogador
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.health = settings.player_health

        # Flags de movimento
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Flag de ultimo movimento
        self.last_move = "left"

        self.last_teleport = 0

        # Flag de atirar
        self.fire_rate = settings.player_fire_rate
        self.last_shot = 0

    def update(self):
        """Atualiza a posicao do jogador"""
        if self.moving_right and check_wall(self, self.settings, self.screen, "right"):
            self.centerx += self.settings.player_speed_factor
        elif self.moving_left and check_wall(self, self.settings, self.screen, "left"):
            self.centerx -= self.settings.player_speed_factor
        elif self.moving_up and check_wall(self, self.settings, self.screen, "up"):
            self.centery -= self.settings.player_speed_factor
        elif self.moving_down and check_wall(self, self.settings, self.screen, "down"):
            self.centery += self.settings.player_speed_factor
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery
        self.check_teleport(pygame.time.get_ticks())

    def blitme(self):
        """Desenha o jogador em sua posicao atual"""
        # se o jogador estiver se movendo para a direita
        # flipa a imgagem para a direita
        if self.moving_right and not self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = True
        # se o jogador estiver se movendo para a esquerda
        elif self.moving_left and self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = False

        self.screen.blit(self.image, self.rect)

    def check_teleport(self, time):
        # teleporta a cada 3 seg
        if time - self.last_teleport > 3000:
            if self.rect.center == self.settings.left_tp_position:
                self.last_teleport = time
                self.centerx = self.settings.right_tp_position[0]
                self.centery = self.settings.right_tp_position[1]
            elif self.rect.center == self.settings.right_tp_position:
                self.last_teleport = time
                self.centerx = self.settings.left_tp_position[0]
                self.centery = self.settings.left_tp_position[1]
