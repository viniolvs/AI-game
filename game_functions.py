import sys
import pygame
from collision import check_wall_bullet
from bullet import Bullet
from enemy import Enemy


def end_game(screen):
    pygame.font.init()
    my_font = pygame.font.Font("font.ttf", 100)
    text = my_font.render("Game Over", True, (255, 255, 255))
    screen.blit(
        text, (screen.get_rect().centerx - 300, screen.get_rect().centery - 100)
    )
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
                break
            elif event.key == pygame.K_r:
                return True


def check_keydown_events(event, settings, screen, player, bullets):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        player.moving_right = True
        player.last_move = "right"
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        player.moving_left = True
        player.last_move = "left"
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        player.moving_up = True
        player.last_move = "up"
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        player.moving_down = True
        player.last_move = "down"
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, player, bullets)
    # Fecha o jogo ao apertar Q
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, player):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        player.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        player.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        player.moving_up = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        player.moving_down = False


def check_events(settings, screen, player, bullets):
    """Responde a eventos de pressionamento de teclas e de mouse"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # Move a nave
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, player, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)


def update_screen(settings, screen, map, player, enemies, bullets, round, my_font):
    """Atualiza imagens na tela e alterna para nova tela"""
    # redesenha tela a cada pasagem pelo laço
    screen.fill([255, 255, 255])
    map.blitme()
    player_life_text = my_font.render(
        "Life: " + str(player.health), False, (255, 255, 255)
    )
    round_text = my_font.render("Round: " + str(round), False, (255, 255, 255))
    screen.blit(round_text, (0, 0))
    # exibe no canto superior direito
    screen.blit(player_life_text, ((screen.get_rect().right - 300), 0))

    # redesenha os projeteis
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # desenha o player
    player.blitme()

    # desenha o inimigo
    for enemy in enemies.sprites():
        enemy.blitme()

    # Deixa a tela mais recente visível
    pygame.display.flip()


def update_bullets(bullets, enemies, settings, screen):
    collision = pygame.sprite.groupcollide(bullets, enemies, True, False)

    if collision != {}:
        for key, enemy in collision.items():
            enemy[0].health -= settings.bullet_damage

    bullets.update()

    # remove os projeteis que colidem com as paredes
    for bullet in bullets.copy():
        if not check_wall_bullet(bullet, settings, screen):
            bullets.remove(bullet)


# dispara um projétil
def fire_bullet(settings, screen, player, bullets):
    if (pygame.time.get_ticks() - player.last_shot) > player.fire_rate:
        new_bullet = Bullet(settings, screen, player)
        bullets.add(new_bullet)
        player.last_shot = pygame.time.get_ticks()


# cria a frota de inimigos
# TODO
def spawn_enemies(settings, screen, round, player, enemies):
    enemy1 = Enemy(settings, screen, player, settings.enemy_spawn_1)
    enemy2 = Enemy(settings, screen, player, settings.enemy_spawn_2)
    enemies.add(enemy1)
    enemies.add(enemy2)
