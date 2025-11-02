
class OgmoEntity:

    def __init__(self, name, x, y, values):
        self.name = name
        self.x = x
        self.y = y
        self.values = values

    def X_on_grid(self):
        return int(self.x / 16)
    
    def Y_on_grid(self):
        return int(self.y / 16)

    @classmethod
    def from_json(cls, json_dict):

        instance = cls(
                json_dict['name'],
                json_dict['x'],
                json_dict['y'],
                json_dict['values'])

        return instance
