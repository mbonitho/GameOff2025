
import pygame
from utils.ogmo.ogmoMap import OgmoMap
from gameobjects.entityDefinition import EntityDefinition


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
        self.EnemiesDefinitions: list[EntityDefinition] = []

        self.helpButtonDefinition: EntityDefinition | None = None
        self.vendingMachineDefinition: EntityDefinition | None = None

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

