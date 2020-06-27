from typing import List

from pygame import sprite, Surface, draw, mouse, K_n, event, KEYDOWN, MOUSEBUTTONDOWN, display
from pygame.math import Vector2

from level.room.room import Room
from game_settings import WHITE, GREEN, BLACK, GRAY, YELLOW, RED, WINDOW_HEIGHT, WINDOW_WIDTH


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
        self._dots = sprite.Group()
        num_rows = len(room_manager.rooms_per_row)

        _id = 0

        for i, room_per_row in enumerate(room_manager.rooms_per_row):
            for j in range(0, room_per_row):
                self._dots.add(
                    RoomMarkerUI(
                        (WINDOW_WIDTH*(i+1))/(num_rows+1),
                        WINDOW_HEIGHT*(j+1)/(room_per_row+1),
                        10,
                        _id)
                )
                _id += 1

    def render(self, screen,
               rooms: List[Room],
               moveable_rooms: List[int],
               current_room_id: int,
               set_current_room):

        while True:
            # self._dots.update(rooms)
            for dot, room in zip(self._dots, rooms):
                if room.cleared():
                    dot.image.fill(YELLOW)
                elif room.id == current_room_id:
                    dot.image.fill(RED)
                elif room.id in moveable_rooms:
                    if dot.rect.collidepoint(mouse.get_pos()):
                        dot.image.fill(RED)
                    else:
                        dot.image.fill(WHITE)
                else:
                    dot.image.fill(GRAY)

            screen.fill(BLACK)
            self._dots.draw(screen)
            display.flip()

            for e in event.get():
                if e.type == KEYDOWN and e.key == K_n:
                    return
                if e.type == MOUSEBUTTONDOWN:
                    x, y = e.pos
                    for dot in self._dots:

                        if dot.rect.collidepoint(x, y):
                            set_current_room(dot.id)
                            return
