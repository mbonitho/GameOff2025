import random
from typing import Counter

from gameobjects.room import Room
from utils.ogmo.ogmoHelper import OgmoHelper
from utils.ogmo.ogmoMap import OgmoMap


class Level:

    tile_lookup = {
        0: "1wayD",
        1: "1wayL",
        2: "1wayR",
        3: "1wayU",
        4: "2waysLR",
        5: "2waysUD",
        6: "4ways"
    }

    MAX_SIZE = 8

    def __init__(self, levelFilenameWithoutExtension: str):
        self.Rooms = []
        self.CommTowerPositions: list[tuple[int, int]] = []
        self.ElevatorCoords: tuple[int, int]

        self.StartingRoom = None
        
        # generate each room
        levelMap = OgmoHelper.get_map(levelFilenameWithoutExtension, 'levels')
        eventLayer = levelMap.layers['roomsEvents']

        for index, value in enumerate(levelMap.layers['rooms'].data):
            if value >= 0:
                mapName = Level.tile_lookup[value]

                y_in_tileset, x_in_tileset = divmod(index, levelMap.layers['rooms'].gridCellsX)

                room = Room(OgmoHelper.get_map(mapName), (x_in_tileset, y_in_tileset))
                room.GenerateObstacles()
                self.Rooms.append(room)

                for entity in eventLayer.entities.copy():

                    x = int(entity.x / eventLayer.gridCellWidth) 
                    y = int(entity.y / eventLayer.gridCellHeight) 

                    if x_in_tileset == x and y_in_tileset == y:

                        match(entity.name):

                            case 'roomStart':
                                self.StartingRoom = room

                            case 'roomAntenna':
                                self.CommTowerPositions.append((x, y))

                            case 'roomStairsUp':
                                self.ElevatorCoords = (x, y)

                        eventLayer.entities.remove(entity)


    def GetRoomByCoords(self, x: int, y: int) -> Room | None:
        return next(room for room in self.Rooms if room.Coords == (x,y))

