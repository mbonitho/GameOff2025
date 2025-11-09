import random
from typing import Counter

import pygame
from utils.ogmo.ogmoHelper import OgmoHelper
from utils.ogmo.ogmoMap import OgmoMap


class Room:

    def __init__(self, map: OgmoMap, coords: tuple[int, int]):
        self.Map = map

        self.RoomLeft: Room | None = None
        self.RoomRight: Room | None = None
        self.RoomUp: Room | None = None
        self.RoomDown: Room | None = None
        self.Coords = coords

        self.Occupied = False

        self.Cleared = False

        self.Obstacles = []

        # block walls
        match map.name:
            case '2waysUD':
                self.RoomLeft = Room(OgmoMap(), (-1, -1))
                self.RoomRight = Room(OgmoMap(), (-1, -1))
            case '2waysLR':
                self.RoomUp = Room(OgmoMap(), (-1, -1))
                self.RoomDown = Room(OgmoMap(), (-1, -1))
            case '1wayU':
                self.RoomDown = Room(OgmoMap(), (-1, -1))
                self.RoomLeft = Room(OgmoMap(), (-1, -1))
                self.RoomRight = Room(OgmoMap(), (-1, -1))
            case '1wayD':
                self.RoomUp = Room(OgmoMap(), (-1, -1))
                self.RoomLeft = Room(OgmoMap(), (-1, -1))
                self.RoomRight = Room(OgmoMap(), (-1, -1))
            case '1wayL':
                self.RoomUp = Room(OgmoMap(), (-1, -1))
                self.RoomDown = Room(OgmoMap(), (-1, -1))
                self.RoomRight = Room(OgmoMap(), (-1, -1))
            case '1wayR':
                self.RoomUp = Room(OgmoMap(), (-1, -1))
                self.RoomDown = Room(OgmoMap(), (-1, -1))
                self.RoomLeft = Room(OgmoMap(), (-1, -1))


    def GenerateObstacles(self):
        self.Obstacles = []
        layer = self.Map.layers['walls']
        y_to_draw_to = 0
        for y in range(layer.gridCellsY):
            x_to_draw_to = 0
            for x in range(layer.gridCellsX):
                index = y * layer.gridCellsX + x 
                data = layer.data[index]
                if data != -1:
                    self.Obstacles.append(pygame.Rect(x_to_draw_to, y_to_draw_to, layer.gridCellWidth, layer.gridCellHeight))
                x_to_draw_to += layer.gridCellWidth
            y_to_draw_to += layer.gridCellHeight


class Level:

    MAX_SIZE = 8

    def __init__(self):
        self.Rooms = []
        self.CommTowerPositions: list[tuple[int, int]] = []

        overlappingCoords = [coord for coord, count in Counter(room.Coords for room in self.Rooms).items() if count > 1] 
        attempt = 1
        while len(self.Rooms) < Level.MAX_SIZE or (overlappingCoords and (-1, -1) not in overlappingCoords):
            print(f'Generation attempt {attempt}')
            self.GenerateDungeon()
            attempt += 1

        # when generation is successfull, generate all the obstacles
        for room in self.Rooms:
            room.GenerateObstacles()

        # add a few towers
        for i in range(4):
            oneWayUnoccupiedRoom = random.choice([room for room in self.Rooms if room.Map.name.startswith('1way') and not room.Occupied])
            oneWayUnoccupiedRoom.Occupied = True
            self.CommTowerPositions.append(oneWayUnoccupiedRoom.Coords)

    def GenerateDungeon(self):
        self.Rooms = []
        self.Rooms.append(Room(OgmoHelper.get_map('4ways'), (0,0)))


        # generate rooms right
        while any(room.RoomRight is None for room in self.Rooms):
            
            # pick a random room
            candidates = [room for room in self.Rooms if room.RoomRight is None]
            selected_room: Room = random.choice(candidates)

            if len(self.Rooms) < Level.MAX_SIZE:
                rng = random.randint(1,6)

                if rng >= 1 and rng <= 3:
                    selected_room.RoomRight = Room(OgmoHelper.get_map('2waysLR'), (selected_room.Coords[0] + 1, selected_room.Coords[1]))
                    selected_room.RoomRight.RoomLeft = selected_room
                elif rng >= 4 and rng <= 5:
                    selected_room.RoomRight = Room(OgmoHelper.get_map('1wayL'), (selected_room.Coords[0] + 1, selected_room.Coords[1]))
                    selected_room.RoomRight.RoomLeft = selected_room
                elif rng == 6:
                    selected_room.RoomRight = Room(OgmoHelper.get_map('4ways'), (selected_room.Coords[0] + 1, selected_room.Coords[1]))
                    selected_room.RoomRight.RoomLeft = selected_room
            else:
                selected_room.RoomRight = Room(OgmoHelper.get_map('1wayL'), (selected_room.Coords[0] + 1, selected_room.Coords[1]))
                selected_room.RoomRight.RoomLeft = selected_room

            self.Rooms.append(selected_room.RoomRight)

        # generate rooms left
        while any(room.RoomLeft is None for room in self.Rooms):
            
            # pick a random room
            candidates = [room for room in self.Rooms if room.RoomLeft is None]
            selected_room: Room = random.choice(candidates)

            if len(self.Rooms) < Level.MAX_SIZE:
                rng = random.randint(1,6)

                if rng >= 1 and rng <= 3:
                    selected_room.RoomLeft = Room(OgmoHelper.get_map('2waysLR'), (selected_room.Coords[0] - 1, selected_room.Coords[1]))
                    selected_room.RoomLeft.RoomRight = selected_room
                elif rng >= 4 and rng <= 5:
                    selected_room.RoomLeft = Room(OgmoHelper.get_map('1wayR'), (selected_room.Coords[0] - 1, selected_room.Coords[1]))
                    selected_room.RoomLeft.RoomRight = selected_room
                elif rng == 6:
                    selected_room.RoomLeft = Room(OgmoHelper.get_map('4ways'), (selected_room.Coords[0] - 1, selected_room.Coords[1]))
                    selected_room.RoomLeft.RoomRight = selected_room
            else:
                selected_room.RoomLeft = Room(OgmoHelper.get_map('1wayR'), (selected_room.Coords[0] - 1, selected_room.Coords[1]))
                selected_room.RoomLeft.RoomRight = selected_room

            self.Rooms.append(selected_room.RoomLeft)

        # generate rooms up
        while any(room.RoomUp is None for room in self.Rooms):
            
            # pick a random room
            candidates = [room for room in self.Rooms if room.RoomUp is None]
            selected_room: Room = random.choice(candidates)

            if len(self.Rooms) < Level.MAX_SIZE:
                rng = random.randint(1,6)

                if rng >= 1 and rng <= 3:
                    selected_room.RoomUp = Room(OgmoHelper.get_map('2waysUD'), (selected_room.Coords[0], selected_room.Coords[1] - 1))
                    selected_room.RoomUp.RoomDown = selected_room
                elif rng >= 4 and rng <= 5:
                    selected_room.RoomUp = Room(OgmoHelper.get_map('1wayD'), (selected_room.Coords[0], selected_room.Coords[1] - 1))
                    selected_room.RoomUp.RoomDown = selected_room
                elif rng == 6:
                    selected_room.RoomUp = Room(OgmoHelper.get_map('4ways'), (selected_room.Coords[0], selected_room.Coords[1] - 1))
                    selected_room.RoomUp.RoomDown = selected_room
            else:
                selected_room.RoomUp = Room(OgmoHelper.get_map('1wayD'), (selected_room.Coords[0], selected_room.Coords[1] - 1))
                selected_room.RoomUp.RoomDown = selected_room

            self.Rooms.append(selected_room.RoomUp)

        # generate rooms down
        while any(room.RoomDown is None for room in self.Rooms):
            
            # pick a random room
            candidates = [room for room in self.Rooms if room.RoomDown is None]
            selected_room: Room = random.choice(candidates)

            if len(self.Rooms) < Level.MAX_SIZE:
                rng = random.randint(1,6)

                if rng >= 1 and rng <= 3:
                    selected_room.RoomDown = Room(OgmoHelper.get_map('2waysUD'), (selected_room.Coords[0], selected_room.Coords[1] + 1))
                    selected_room.RoomDown.RoomUp = selected_room
                elif rng >= 4 and rng <= 5:
                    selected_room.RoomDown = Room(OgmoHelper.get_map('1wayU'), (selected_room.Coords[0], selected_room.Coords[1] + 1))
                    selected_room.RoomDown.RoomUp = selected_room
                elif rng == 6:
                    selected_room.RoomDown = Room(OgmoHelper.get_map('4ways'), (selected_room.Coords[0], selected_room.Coords[1] + 1))
                    selected_room.RoomDown.RoomUp = selected_room
            else:
                selected_room.RoomDown = Room(OgmoHelper.get_map('1wayU'), (selected_room.Coords[0], selected_room.Coords[1] + 1))
                selected_room.RoomDown.RoomUp = selected_room

            self.Rooms.append(selected_room.RoomDown)