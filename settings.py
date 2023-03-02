class Settings:
    # Inicializa as configuracoes do jogo
    def __init__(self, screen):
        # Mapa
        self.map_size = (screen.get_width(), screen.get_height())
        self.tile_size = 40
        self.left_tp_position = (80, 570)
        self.right_tp_position = (1850, 540)

        # branco
        self.bg_color = (199, 50, 57)
        self.exit_color = (0, 0, 0)
        self.entry_color = (255, 255, 255)

        # configuracoes do jogador
        self.player_speed_factor = 2
        self.player_size = (50, 50)
        self.player_fire_rate = 500  # 0.5 seg
        self.player_health = 5
        self.player_low_health = self.player_health * 0.25

        # configuracoes do inimigo
        self.enemy_speed_factor = 1
        self.enemy_size = (50, 50)
        self.enemy_health = 1
        self.enemy_low_health = self.enemy_health * 0.25
        self.enemy_attack_rate = 1000  # 1 seg
        self.enemy_attack_damage = 1
        self.enemy_hunt_distance = 200
        self.enemy_spawn_rate = 5000  # 5 seg
        self.enemy_spawn_1 = [
            screen.get_rect().centery,
            screen.get_rect().centerx / 2 - 100,
        ]
        self.enemy_spawn_2 = [
            screen.get_rect().centery,
            screen.get_rect().centerx / 2 * 3 + 100,
        ]

        # configuracoes dos projeteis
        self.bullet_speed_factor = 5
        self.bullet_width = 6
        self.bullet_height = 6
        self.bullet_color = (40, 40, 40)
        self.bullet_damage = 1
