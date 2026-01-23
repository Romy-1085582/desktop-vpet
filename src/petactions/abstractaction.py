import pygame

class AbstractAction:
    def __init__(self, duration, frames, frames_duration, valid_moods):
        self.duration = duration  # Duration of the action in seconds
        self.frames = frames  # List of frames for the action
        self.current_frame = 0
        self.frames_duration = frames_duration  # Duration of each frame in percentage of the total duration
        self.frames_duration_in_seconds = [duration * duration for duration in frames_duration]
        self.valid_moods = valid_moods  # List of valid moods for the action

        self.duration_remaining = duration # Time remaining for the action

        self.valid_action = True # Flag to indicate if the action is valid

        try:
            self.check_valid_inputs()
        except ValueError as e:
            print(f"Invalid input: {e}")
            self.valid_action = False

    def check_valid_inputs(self):
        if not isinstance(self.duration, (int, float)) or self.duration <= 0:
            raise ValueError("Duration must be a positive number.")
        if not isinstance(self.frames, list) or len(self.frames) == 0:
            raise ValueError("Frames must be a non-empty list.")
        if not all(isinstance(frame, pygame.Surface) for frame in self.frames):
            raise ValueError("All frames must be pygame.Surface objects.")
        if not isinstance(self.valid_moods, list):
            raise ValueError("valid_moods must be a list.")
        if self.frames_duration and len(self.frames_duration) != len(self.frames):
            raise ValueError("Length of frames_duration must match length of frames.")
        if not all(isinstance(duration, (int, float)) and duration > 0 for duration in self.frames_duration):
            raise ValueError("All frame durations must be positive numbers.")
        

    def update(self, dt):
        if not self.valid_action:
            return True #end action
        self.duration_remaining -= dt
        if self.duration_remaining <= 0:
            return True  # Action is complete
        if self.current_frame < len(self.frames): #Ensure current_frame is within bounds
            # Check if the duration remaining of this action is more than the duration of the current frame plus all previous frames
            if self.duration_remaining > sum(self.frames_duration_in_seconds[:self.current_frame]):
                self.current_frame += 1
        return False
    

    def draw(self, surface):
        if self.valid_action:
            if self.current_frame < len(self.frames):
                surface.blit(self.frames[self.current_frame], (0, 0))