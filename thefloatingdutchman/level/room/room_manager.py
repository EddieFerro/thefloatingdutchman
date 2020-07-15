from typing import List
from random import randint, choices
from ordered_set import OrderedSet

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

    def _generate_default_graph(self):
        self._number_of_rooms = 11
        self.rooms_per_col.append(1)  # 0
        self.rooms_per_col.append(2)  # 1, 2
        self.rooms_per_col.append(4)  # 3, 4, 5, 6
        self.rooms_per_col.append(3)  # 7, 8, 9
        self.rooms_per_col.append(1)  # 10
        self._room_graph.add_edges_from(
            [(0, 1), (0, 2), (1, 3), (1, 4), (1, 5), (2, 5),
             (2, 6), (3, 7), (4, 7), (5, 8), (6, 9),
             (7, 10), (8, 10), (9, 10)
             ])

    def _generate_room_graph(self, num_rooms, max_per_col):
        self._number_of_rooms = num_rooms

        for i in range(0, self._number_of_rooms):
            self._rooms.append(Room())

        # first and last col should always have 1
        self.rooms_per_col.append(1)  # 0

        rooms_left = self._number_of_rooms - 2

        while rooms_left >= max_per_col+1:
            temp = randint(2, max_per_col)
            self._rooms_per_col.append(temp)
            rooms_left -= temp

        if rooms_left == 1:
            rooms_left += 1
            self._number_of_rooms += 1

        self._rooms_per_col.append(rooms_left)
        self.rooms_per_col.append(1)  # 10

        first_in_col = 0
        for i, room_count in enumerate(self.rooms_per_col):

            next_room_count = self.rooms_per_col[i+1]
            first_in_next_col = first_in_col+room_count
            last_in_col = first_in_next_col-1
            next_col_range = range(
                first_in_next_col, first_in_next_col + next_room_count)

            if i == len(self.rooms_per_col) - 2:
                for _id in range(first_in_col, last_in_col+1):
                    self._room_graph.add_edge(_id, first_in_next_col)

                break

            if room_count > 1:

                self._room_graph.add_edge(first_in_col, first_in_next_col)

                self._room_graph.add_edge(
                    last_in_col, last_in_col+next_room_count)

                chosen_ids = choices(next_col_range, k=room_count-2)
                chosen_ids.sort()

                # picks inside nodes from current col to join to next col
                for index, _id in enumerate(chosen_ids):
                    self._room_graph.add_edge(first_in_col+1+index, _id)

                chosen_ids.insert(0, first_in_next_col)
                chosen_ids.append(first_in_next_col + next_room_count - 1)

                inner_next_col_ids = set(next_col_range)

                # removes first and last from next column set
                inner_next_col_ids.remove(first_in_next_col)

                if next_room_count != 1:
                    inner_next_col_ids.remove(
                        first_in_next_col + next_room_count - 1)

                not_sel_list = list(inner_next_col_ids - set(chosen_ids))
                not_sel_list.sort(reverse=True)
                not_selected = OrderedSet(not_sel_list)

                # while we have nodes not selected
                while not_selected:
                    _id = not_selected.pop()
                    j = _id - 1
                    k = _id

                    node_set = OrderedSet([_id])

                    j_index = [i for i, chosen_id in enumerate(
                        chosen_ids) if chosen_id == j][-1]

                    node_j_id = j_index + first_in_col

                    while k not in chosen_ids:
                        k += 1

                        if k not in chosen_ids:
                            node_set.add(k)
                            not_selected.pop()

                    k_index = chosen_ids.index(k)
                    node_k_id = k_index + first_in_col

                    choosy_listy = choices(
                        range(node_j_id, node_k_id+1), k=len(node_set))
                    choosy_listy.sort()

                    for nodey_boy, nodey_girl in zip(choosy_listy, node_set):
                        self._room_graph.add_edge(nodey_boy, nodey_girl)

            else:
                for _id in next_col_range:
                    self._room_graph.add_edge(first_in_col, _id)

            first_in_col += room_count

    def spawn(self, level: int):
        self._rooms = []
        self._rooms_per_col = []
        self._current_room_id = 0

        self._room_graph.clear()
        self._generate_room_graph(26, 5)

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
