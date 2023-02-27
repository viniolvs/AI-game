import pygame
import random
from collision import check_wall
from pygame.sprite import Sprite
from math import sqrt


class Enemy(Sprite):
    """Representa um inimigo"""

    def __init__(self, settings, screen, player, position):
        super(Enemy, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load("images/zombie.png")
        self.image = pygame.transform.scale(self.image, settings.enemy_size)
        # self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.rect.top = self.image.get_rect().top
        self.screen_rect = screen.get_rect()

        # Posicao inicial do inimigo
        self.rect.centerx = position[1]
        self.rect.centery = position[0]
        self.rect.center = self.rect.centerx, self.rect.centery
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.health = settings.enemy_health

        self.last_attack = 0

        self.last_state = "idle"

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.best_move = []

        self.player = player

    def blitme(self):
        """Desenha o inimigo na tela"""
        self.screen.blit(self.image, self.rect)

    def hunt_distance(self):
        """Calcula a distancia entre o player e o inimigo"""
        distance = sqrt(
            (self.centerx - self.player.rect.centerx) ** 2
            + (self.centery - self.player.rect.centery) ** 2
        )
        if distance <= self.settings.enemy_hunt_distance:
            return True
        return False

    def set_state(self):
        if self.health <= 0:
            self.kill()
        # ataca quando está próximo do player
        elif self.rect.colliderect(self.player.rect):
            self.attack()
        # caça quando a vida do player está em 20%
        elif self.player.health <= self.settings.player_low_health:
            self.hunt()
        # cura quando a vida está em 20%
        elif self.health <= self.settings.enemy_low_health:
            self.low()
        # caça quando está à uma distancia de 20% do player
        elif self.hunt_distance():
            self.hunt()
        else:
            self.idle()

    def update(self):
        self.set_state()

    def idle(self):
        print("idle")
        if self.last_state != "idle":
            self.restart_move()
        self.enemy_random_move()
        self.last_state = "idle"

    def hunt(self):
        print("hunt")
        if self.last_state != "hunt":
            self.restart_move()
        self.a_star_move()
        self.last_state = "hunt"

    def attack(self):
        if (
            pygame.time.get_ticks() - self.last_attack
        ) > self.settings.enemy_attack_rate:
            self.player.health -= 1
            self.last_attack = pygame.time.get_ticks()
            print("attacked")
        self.last_state = "attack"

    def low(self):
        print("low")
        # inimigo foge do player
        if self.last_state != "low":
            self.restart_move()
        self.a_star_move(True)
        self.last_state = "low"

    def restart_move(self):
        self.best_move = []
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def move(self, margin=30):
        if self.moving_right:
            if check_wall(self, self.settings, self.screen, "right", margin):
                self.centerx += self.settings.enemy_speed_factor
            else:
                self.moving_right = False
        elif self.moving_left:
            if check_wall(self, self.settings, self.screen, "left", margin):
                self.centerx -= self.settings.enemy_speed_factor
            else:
                self.moving_left = False
        elif self.moving_up:
            if check_wall(self, self.settings, self.screen, "up", margin):
                self.centery -= self.settings.enemy_speed_factor
            else:
                self.moving_up = False
        elif self.moving_down:
            if check_wall(self, self.settings, self.screen, "down", margin):
                self.centery += self.settings.enemy_speed_factor
            else:
                self.moving_down = False
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def enemy_random_move(self):
        """Move the enemy in a random direction."""
        if (
            not self.moving_right
            and not self.moving_left
            and not self.moving_up
            and not self.moving_down
        ):
            random_direction = random.randint(1, 4)
            if random_direction == 1:
                self.moving_right = True
            elif random_direction == 2:
                self.moving_left = True
            elif random_direction == 3:
                self.moving_up = True
            else:
                self.moving_down = True
        self.move()

    def get_possible_moves(self):
        possible_moves = []
        margin = 30
        if check_wall(self, self.settings, self.screen, "right", margin):
            possible_moves.append(
                [self.rect.centerx + margin, self.rect.centery, "right"]
            )
        if check_wall(self, self.settings, self.screen, "left", margin):
            possible_moves.append(
                [self.rect.centerx - margin, self.rect.centery, "left"]
            )
        if check_wall(self, self.settings, self.screen, "up", margin):
            possible_moves.append([self.rect.centerx, self.rect.centery - margin, "up"])
        if check_wall(self, self.settings, self.screen, "down", margin):
            possible_moves.append(
                [self.rect.centerx, self.rect.centery + margin, "down"]
            )
        return possible_moves

    def get_best_move(self, heal=False):
        possible_moves = self.get_possible_moves()
        player_pos = self.player.rect.center
        best_move = [possible_moves[0][0], possible_moves[0][1], possible_moves[0][2]]
        best_move_distance = -1
        for move in possible_moves:
            distance = sqrt(
                (move[0] - player_pos[0]) ** 2 + (move[1] - player_pos[1]) ** 2
            )
            if heal:
                if best_move_distance == -1 or distance > best_move_distance:
                    best_move_distance = distance
                    best_move = move
            else:
                if best_move_distance == -1 or distance < best_move_distance:
                    best_move_distance = distance
                    best_move = move
        self.best_move = best_move

    def a_star_move(self, heal=False):
        # Método A* para movimentação do inimigo
        if self.best_move == []:
            self.get_best_move(heal)
        else:
            if (
                self.rect.centerx == self.best_move[0]
                and self.rect.centery == self.best_move[1]
            ):
                self.restart_move()
            else:
                if self.best_move[2] == "right":
                    self.moving_right = True
                elif self.best_move[2] == "left":
                    self.moving_left = True
                elif self.best_move[2] == "up":
                    self.moving_up = True
                elif self.best_move[2] == "down":
                    self.moving_down = True
            self.move(0)
