from typing import List
from random import randint, sample

import networkx as nx
from pygame import Surface

from manager import Manager
from level.room.room import Room
from character.player.player_sprite import PlayerSprite
from character.enemy.enemy_sprite import EnemySprite


class RoomManager(Manager):
    def __init__(self):
        super().__init__()
        self._number_of_rooms = 0
        self._rooms = []
        self._rooms_per_col = []
        self._room_graph = nx.DiGraph()
        self._current_room_id = 0

    def _generate_room_graph(self):
        self._number_of_rooms = 11

        for i in range(0, self._number_of_rooms):
            self._rooms.append(Room())

        # room_cols = 5 == len(self.rooms_per_col)
        # first and last col should always have 1
        # self.rooms_per_col.append(1)  # 0
        # self.rooms_per_col.append(2)  # 1, 2
        # self.rooms_per_col.append(4)  # 3, 4, 5, 6
        # self.rooms_per_col.append(3)  # 7, 8, 9
        # self.rooms_per_col.append(1)  # 10

        self.rooms_per_col.append(1)  # 0

        max_per_col = 4
        rooms_left = self._number_of_rooms - 2
        
        while rooms_left > max_per_col+1:
            temp = randint(2, max_per_col)
            self._rooms_per_col.append(temp)
            rooms_left -= temp

        self._rooms_per_col.append(rooms_left)
        self.rooms_per_col.append(1)  # 10

        print("ROOMS PER COL: ", self._rooms_per_col)

        first_in_col = 0
        for i, room_count in enumerate(self.rooms_per_col):
            if i == len(self.rooms_per_col) - 1:
                break

            next_room_count = self.rooms_per_col[i+1]
            last_in_col = first_in_col+room_count-1

            self._room_graph.add_edge(first_in_col, last_in_col+1)
            if room_count > 1:
                self._room_graph.add_edge(last_in_col, last_in_col+next_room_count)

                
                if room_count > 2 and room_count-2 <= next_room_count:
                    print("ROOM COUNT: " + str(room_count))
                    print("Next Room Count: " + str(next_room_count))
                    print('last in column: ' + str(last_in_col))
                    print("end of range: " + str(last_in_col+1+next_room_count))
            
                    paths = sample(range(last_in_col+1, last_in_col+1+next_room_count), room_count-2)
                    paths.sort()
                    print(paths)
                    for index, _id in enumerate(paths):
                        self._room_graph.add_edge(first_in_col+1+index, _id)
            
            
            first_in_col += room_count

        
        print(self._room_graph)

        # self._room_graph.add_edges_from(
        #     [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 5),
        #      (2, 6), (3, 7), (4, 7), (5, 8), (6, 9),
        #      (7, 10), (8, 10), (9, 10)
        #      ])

    def spawn(self, level: int):
        self._rooms = []
        self._rooms_per_col = []
        self._current_room_id = 0

        self._room_graph.clear()
        self._generate_room_graph()

        for i, room in enumerate(self._rooms):
            room.spawn(level, i)

    def get_available_rooms(self) -> List[int]:

        # room must be cleared to move on
        if not self._rooms[self._current_room_id].cleared():
            return []

        # gets pairs of edges from current room to next available rooms
        edges = self._room_graph.edges(self._current_room_id)

        # gets list of rooms player can move to next
        return [v2 for v1, v2 in edges]

    def is_level_cleared(self) -> bool:

        return self._rooms[self.current_room_id].cleared() and not self.get_available_rooms()

    def set_current_room(self, _id: int):
        # TODO(kayton): Add checks to ensure id is valid
        self._current_room_id = _id

    def update(self, player: PlayerSprite, screen: Surface):
        self._rooms[self._current_room_id].update(player, screen)

    def draw(self, screen):
        self._rooms[self._current_room_id].draw(screen)

    def get_current_enemies(self) -> List[EnemySprite]:
        return self.rooms[self.current_room_id].get_enemies()

    @property
    def current_room_id(self):
        return self._current_room_id

    @property
    def rooms(self) -> List[Room]:
        return self._rooms

    @property
    def rooms_per_col(self) -> List[int]:
        return self._rooms_per_col
