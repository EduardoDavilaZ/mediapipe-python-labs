import cv2
import config.config as settings

class Keyboard:
    """
    Handles the piano layout generation, collision detection with hand landmarks,
    and visual rendering of the keyboard on the video frame.
    """
    def __init__(self, octaves=[3, 4, 5]):
        self.octaves = octaves
        self.white_keys = []
        self.black_keys = []
        
        # Musical note mapping
        white_names = ["C", "D", "E", "F", "G", "A", "B"]
        black_names = ["C#", "D#", "F#", "G#", "A#"]
        
        # Layout calculations
        total_white = len(white_names) * len(octaves)
        self.w_width = settings.WIDTH // total_white
        self.w_height = 250
        y_pos = settings.HEIGHT - self.w_height

        # Generate white keys
        for i, oct in enumerate(octaves):
            for j, name in enumerate(white_names):
                note_id = f"{name}{oct}"
                x = (i * len(white_names) + j) * self.w_width
                self.white_keys.append({
                    "note": note_id,
                    "rect": [x, y_pos, self.w_width, self.w_height],
                })

        # Generate black keys
        for i, oct in enumerate(octaves):
            # Positioning logic for black keys between white keys
            positions = [1, 2, 4, 5, 6] 
            for pos, name in zip(positions, black_names):
                white_idx = (i * 7) + pos
                x = (white_idx * self.w_width) - (self.w_width // 4)
                self.black_keys.append({
                    "note": f"{name}{oct}",
                    "rect": [x, y_pos, self.w_width // 2, self.w_height // 2],
                })

    def is_finger_pressing(self, landmarks, tip_id):
        """
        Determines if a finger is in a 'pressed' state.
        A finger is considered pressing if the tip is lower (higher Y value) 
        than the finger's PIP joint.
        """
        # Thumb(4) uses MCP joint(3), others use PIP joint(tip - 2)
        joint_id = tip_id - 2 if tip_id != 4 else 3
        return landmarks[tip_id][1] > landmarks[joint_id][1]

    def check_collision(self, landmarks, tip_id):
        """
        Checks if a specific finger tip is colliding with any key.
        Returns the note ID if a collision occurs, otherwise None.
        """
        if not self.is_finger_pressing(landmarks, tip_id):
            return None

        px, py, _ = landmarks[tip_id]

        # Check black keys first (higher priority in layering)
        for key in self.black_keys:
            x, y, w, h = key["rect"]
            if x < px < x + w and y < py < y + h:
                return key["note"]

        # Check white keys
        for key in self.white_keys:
            x, y, w, h = key["rect"]
            if x < px < x + w and y < py < y + h:
                return key["note"]
                
        return None

    def draw(self, frame, active_notes):
        """
        Renders the keyboard on the provided video frame.
        Active keys are highlighted with the configured pressed color.
        """
        # 1. Draw white keys
        for key in self.white_keys:
            x, y, w, h = key["rect"]
            is_active = key["note"] in active_notes
            
            # Use pressed color if active, otherwise draw outline
            if is_active:
                cv2.rectangle(frame, (x, y), (x + w, y + h), settings.PRESSED_KEY_COLOR, -1)
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), settings.WHITE_KEY_COLOR, 2)
            
            # Label the note
            cv2.putText(frame, key["note"], (x + 5, y + h - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)

        # 2. Draw black keys
        for key in self.black_keys:
            x, y, w, h = key["rect"]
            is_active = key["note"] in active_notes
            color = settings.PRESSED_KEY_COLOR if is_active else settings.BLACK_KEY_COLOR
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)