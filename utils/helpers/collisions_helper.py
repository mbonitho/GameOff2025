

from pygame import Rect


def MoveAndCollide(rect: Rect, dx: int, dy: int, obstacles: list[Rect]):
    collisions = (0, 0)
    if dx != 0:
        rect.x += dx
        # separate entity from obstacles
        for wall in obstacles:
            if rect.colliderect(wall):
                collisions = (1, collisions[1])
                if rect.x < wall.x:  # moving right
                    rect.right = wall.left
                elif rect.right > wall.right:  # moving left
                    rect.left = wall.right
                break
    if dy != 0:
        rect.y += dy
        for wall in obstacles:
            if rect.colliderect(wall):
                collisions = (collisions[0], 1)
                if rect.top < wall.top:  # moving down
                    rect.bottom = wall.top
                elif rect.bottom > wall.bottom:  # moving up
                    rect.top = wall.bottom
                break

    return collisions