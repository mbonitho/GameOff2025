import random
from typing import Counter

from gameobjects.room import Room
from utils.ogmo.ogmoHelper import OgmoHelper
from utils.ogmo.ogmoMap import OgmoMap
from gameobjects.enemyDefinition import EnemyDefinition

class Level:

    tile_lookup = {
        0: "1wayD",
        1: "1wayL",
        2: "1wayR",
        3: "1wayU",
        4: "2waysLR",
        5: "2waysUD",
        6: "4ways",
        7: "2waysLU",
        8: "2waysUR",
        9: "2waysRD",
        10: "2waysDL",
        11: "3waysLUD",
        12: "3waysLUR",
        13: "3waysURD",
        14: "3waysLRD",
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
        roomLayer = levelMap.layers['rooms']
        for index, value in enumerate(roomLayer.data):
            if value >= 0:
                mapName = Level.tile_lookup[value]

                y_in_tileset, x_in_tileset = divmod(index, levelMap.layers['rooms'].gridCellsX)

                room = Room(OgmoHelper.get_map(mapName), (x_in_tileset, y_in_tileset))
                room.GenerateObstacles()
                self.Rooms.append(room)

                for entity in eventLayer.entities.copy():

                    x_in_level_grid = int(entity.x / roomLayer.gridCellWidth) 
                    y_in_level_grid = int(entity.y / roomLayer.gridCellHeight)

                    if x_in_tileset == x_in_level_grid and y_in_tileset == y_in_level_grid:

                        match(entity.name):

                            case 'roomStart':
                                self.StartingRoom = room

                            case 'roomAntenna':
                                self.CommTowerPositions.append((x_in_level_grid, y_in_level_grid))

                            case 'roomStairsUp':
                                self.ElevatorCoords = (x_in_level_grid, y_in_level_grid)

                            case 'enemy':
                                x_in_map_grid = (((entity.x % roomLayer.gridCellWidth) / eventLayer.gridCellWidth) + 1) / 16 
                                y_in_map_grid = (((entity.y % roomLayer.gridCellHeight) / eventLayer.gridCellHeight) + 1) / 16

                                room.EnemiesDefinitions.append(EnemyDefinition(entity.values['Type'], (x_in_map_grid,y_in_map_grid)))

                        eventLayer.entities.remove(entity)


    def GetRoomByCoords(self, x: int, y: int) -> Room | None:
        return next(room for room in self.Rooms if room.Coords == (x,y))

