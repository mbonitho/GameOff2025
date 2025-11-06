import pygame

def tint_surface(surface, tint_color, alpha=128):
    tinted = surface.copy()
    tint = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    tint.fill(tint_color + (alpha,))
    tinted.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted
