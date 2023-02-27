import pygame
from enemy import Enemy
from settings import Settings
from map import Map
from player import Player
from pygame.sprite import Group
import game_functions as gf


def run_game():
    # Inicializa o jogo e cria um objeto para a tela
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # Cria uma instância para o mapa
    settings = Settings(screen)
    map = Map(settings, screen)

    player = Player(settings, screen)
    bullets = Group()
    enemies = Group()

    my_font = pygame.font.Font("font.ttf", 50)

    round = 1
    i = 1
    last_spawn = 0

    settings.enemy_health = round
    # Inicializa o laço principal do jogo
    gf.spawn_enemies(settings, screen, round, player, enemies)
    while True:

        if player.health <= 0:
            break
        time = pygame.time.get_ticks()
        if i < round and time - settings.enemy_spawn_rate > last_spawn:
            gf.spawn_enemies(settings, screen, round, player, enemies)
            last_spawn = time
            i += 1
        if i > 0 and enemies.sprites() == []:
            round += 1
            settings.enemy_health = round
            if round % 2 == 0 and player.fire_rate > 100:
                player.fire_rate -= 100
            if round % 3 == 0 and settings.player_speed_factor < 20:
                settings.player_speed_factor += 1
            if round % 4 == 0:
                if settings.bullet_damage == 1:
                    settings.bullet_damage += 1
                else:
                    settings.bullet_damage += 2
            if round % 5 == 0:
                settings.player_health += 1
                player.health = settings.player_health
                settings.bullet_speed_factor += 1
            if player.health < settings.player_health:
                player.health += 1
            i = 1
            gf.spawn_enemies(settings, screen, round, player, enemies)
            last_spawn = time

        gf.check_events(settings, screen, player, bullets)
        player.update()
        enemies.update()
        gf.update_bullets(bullets, enemies, settings, screen)
        gf.update_screen(
            settings, screen, map, player, enemies, bullets, round, my_font
        )
    # exibe a tela de game over e espera o jogador apertar uma tecla
    while True:
        if gf.end_game(screen):
            run_game()


run_game()
