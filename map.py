from pygame.sprite import Group
from tile import Tile


class Map:
    def __init__(self, settings, screen):
        self.settings = settings
        self.map_size = self.settings.map_size
        self.screen = screen
        self.tile_size = self.settings.tile_size
        self.size = self.settings.map_size
        self.walls = Group()
        # divide o mapa em tiles
        self.tiles = Group()
        for y in range(0, self.map_size[1], self.tile_size):
            for x in range(0, self.map_size[0], self.tile_size):
                if y == 0 or y == self.map_size[1] - self.tile_size:
                    tile = Tile(screen, x, y, self.settings, "images/wall.png")
                    tile.is_wall = True
                    self.tiles.add(tile)
                    self.walls.add(tile)
                elif x == 0 or x == self.map_size[0] - self.tile_size:
                    tile = Tile(screen, x, y, self.settings, "images/wall.png")
                    tile.is_wall = True
                    self.tiles.add(tile)
                    self.walls.add(tile)
                else:
                    self.tiles.add(Tile(screen, x, y, self.settings))

    def blitme(self):
        for tile in self.tiles.sprites():
            tile.blitme()
