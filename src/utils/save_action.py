import json

class SaveActions:
    @staticmethod
    def create_new_action(name, description):
        return {
            "name": name, # Action name
            "description": description, # Action description
            "duration": 0, # Time in seconds, float
            "frames_amount": 0, # Amount of frames, integer.
            "frames": {}, #File paths for each frame.
            "frames_duration": [], # List of the durations for each frame, in fractions of 1
            "valid_moods": [] # List of the valid moods for this action
        }
