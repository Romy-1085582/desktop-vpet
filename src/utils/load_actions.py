import json

class LoadActions:
    @staticmethod
    def load_actions_from_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
