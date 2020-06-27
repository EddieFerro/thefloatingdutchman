from pygame import sprite, Surface, draw, mouse, K_n, event, KEYDOWN, display
from pygame.math import Vector2

from game_settings import WHITE, GREEN, BLACK, WINDOW_HEIGHT, WINDOW_WIDTH


class RoomMarkerUI(sprite.Sprite):
    def __init__(self, x: int, y: int, radius: int, id: int):
        sprite.Sprite.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.pos = Vector2(self.x, self.y)
        self.radius = radius
        # Create the circle image
        self.image = Surface((self.radius*2, self.radius*2))
        self.rect = self.image.get_rect(center=self.pos)
        self.image.fill(WHITE)
        draw.circle(self.image, WHITE,
                    (self.radius, self.radius), self.radius)

    def update(self, rooms):
        if self.rect.collidepoint(mouse.get_pos()):
            self.image.fill(GREEN)
        else:
            self.image.fill(WHITE)


class MapUI:
    def __init__(self):
        pass

    def spawn(self, room_manager):

        num_rooms = len(room_manager.rooms)
        print(num_rooms)
        self._dots = sprite.Group()
        num_rows = len(room_manager.rooms_per_row)

        for i, room_per_row in enumerate(room_manager.rooms_per_row):
            for j in range(0, int(room_per_row)):
                self._dots.add(RoomMarkerUI(
                    (WINDOW_WIDTH*(i+1))/(num_rows+1), WINDOW_HEIGHT*(j+1)/(room_per_row+1), 10, i+j))

    def render(self, screen, rooms):
        while True:
            self._dots.update(rooms)
            screen.fill(BLACK)
            self._dots.draw(screen)
            display.flip()

            for e in event.get():
                if e.type == KEYDOWN and e.key == K_n:
                    return
