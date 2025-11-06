
from utils.ogmo.ogmoEntity import OgmoEntity


class OgmoMap:

    def __init__(self, width = 0, height = 0):
        self.name = ''
        self.width = width
        self.height = height

        self.values = {}
        self.layers = {}

    @classmethod
    def from_json(cls, json_dict):
        # dict_keys(['ogmoVersion', 'width', 'height', 'offsetX', 'offsetY', 'values', 'layers'])
        instance = cls(
                json_dict['width'],
                json_dict['height'])

        for layer_dict in json_dict['layers']:
            layer = OgmoLayer.from_json(layer_dict)
            instance.layers[layer.name] = layer
        
        if 'values' in json_dict.keys():
            instance.values = json_dict['values']

        return instance

class OgmoLayer:
    def __init__(self, name, tileset, gridCellsX, gridCellsY, gridCellWidth, gridCellHeight, data):
        self.name = name
        self.tileset = tileset
        self.data = data

        self.values = {}
        self.entities = []

        # width in tiles
        self.gridCellsX = gridCellsX
        self.gridCellsY = gridCellsY

        self.gridCellWidth = gridCellWidth
        self.gridCellHeight = gridCellHeight

    @classmethod
    def from_json(cls, json_dict):
        # dict_keys(['name', '_eid', 'offsetX', 'offsetY', 
        #            'gridCellWidth', 'gridCellHeight', 'gridCellsX', 
        #            'gridCellsY', 'tileset', 'data', 'exportMode', 
        #            'arrayMode'])
        instance = cls(
                json_dict['name'],
                json_dict['tileset'] if 'tileset' in json_dict.keys() else '',
                json_dict['gridCellsX'],
                json_dict['gridCellsY'],
                json_dict['gridCellWidth'],
                json_dict['gridCellHeight'],
                json_dict['data'] if 'data' in json_dict.keys() else [])
        
        #todo les entities
        for entities_dict in json_dict['entities'] if 'entities' in json_dict.keys() else []:
            instance.entities.append(OgmoEntity.from_json(entities_dict))

        if 'values' in json_dict.keys():
            instance.values = json_dict['values']

        return instance