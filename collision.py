from pygame import Surface


def check_color(settings, color):
    """Check if a color is the same as the background color."""
    tolerance = 5
    if (color[0] - tolerance) <= settings.bg_color[0] <= (color[0] + tolerance):
        if (color[1] - tolerance) <= settings.bg_color[1] <= (color[1] + tolerance):
            if (color[2] - tolerance) <= settings.bg_color[2] <= (color[2] + tolerance):
                return True
    return False


def check_wall_bullet(bullet, settings, screen, margin=1):
    """Check if a bullet is touching a wall using background color."""
    centerx = int(bullet.rect.centerx)
    centery = int(bullet.rect.centery)
    top = int(bullet.rect.top)
    bottom = int(bullet.rect.bottom)
    left = int(bullet.rect.left)
    right = int(bullet.rect.right)
    if check_color(
        settings,
        Surface.get_at(screen, (right + margin, centery)),
    ):
        return True
    elif check_color(
        settings,
        Surface.get_at(screen, (left - margin, centery)),
    ):
        return True
    elif check_color(
        settings,
        Surface.get_at(screen, (centerx, top - margin)),
    ):
        return True
    elif check_color(
        settings,
        Surface.get_at(screen, (centerx, bottom + margin)),
    ):
        return True
    return False


def check_wall(character, settings, screen, side, margin=10):
    """Check if a character is touching a wall using background color."""
    centerx = int(character.rect.centerx)
    centery = int(character.rect.centery)
    top = int(character.rect.top)
    bottom = int(character.rect.bottom)
    left = int(character.rect.left)
    right = int(character.rect.right)
    if side == "right":
        return check_color(
            settings,
            Surface.get_at(screen, (right + margin, centery)),
        )
    elif side == "left":
        return check_color(
            settings,
            Surface.get_at(screen, (left - margin, centery)),
        )
    elif side == "up":
        return check_color(
            settings,
            Surface.get_at(screen, (centerx, top - margin)),
        )

    elif side == "down":
        return check_color(
            settings,
            Surface.get_at(screen, (centerx, bottom + margin)),
        )
