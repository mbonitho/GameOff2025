import json
import os

from utils.ogmo.ogmoMap import OgmoMap

class OgmoHelper:

    @classmethod
    def get_map(self, mapFileNameWithoutExtension, sub_folder= 'rooms'):
        full_path = os.path.join('assets', 'maps', sub_folder, f'{mapFileNameWithoutExtension}.json')

        # print(os.getcwd())
        # print(full_path)
        # print(os.path.exists(full_path))
        json_str = ''
        with open(full_path, 'r') as map_file:
            json_str = map_file.read()
        
        data_dict = json.loads(json_str)
        map = OgmoMap.from_json(data_dict)
        map.name = mapFileNameWithoutExtension

        return map