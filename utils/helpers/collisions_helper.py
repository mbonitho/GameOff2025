

from pygame import Rect


def MoveAndCollide(rect: Rect, dx: int, dy: int, obstacles: list[Rect]):

    if dx != 0:
        rect.x += dx
        # separate player from obstacles
        for wall in obstacles:
            if rect.colliderect(wall):
                if rect.x < wall.x:  # moving right
                    rect.right = wall.left
                elif rect.right > wall.right:  # moving left
                    rect.left = wall.right
                break
    if dy != 0:
        rect.y += dy
        for wall in obstacles:
            if rect.colliderect(wall):
                if rect.top < wall.top:  # moving down
                    rect.bottom = wall.top
                elif rect.bottom > wall.bottom:  # moving up
                    rect.top = wall.bottom
                break