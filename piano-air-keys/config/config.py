# Window Dimensions
WIDTH, HEIGHT = 1280, 720
FPS = 60

# Piano Configuration
VISIBLE_OCTAVES = 3  # Adjusted to 3 as we discussed (Octaves 3, 4, 5)
PRESSED_KEY_COLOR = (49, 120, 60)  # Green
WHITE_KEY_COLOR = (255, 255, 255)
BLACK_KEY_COLOR = (0, 0, 0)

# Detection Thresholds
# Z_THRESHOLD: Distance from the camera to detect a "press" 
# (lower values mean closer to the lens)
Z_THRESHOLD = 0.5 

# Hand Landmarks (MediaPipe indices)
INDEX_FINGER_TIP = 8
MIDDLE_FINGER_TIP = 12
THUMB_TIP = 4

# Audio Settings
SAMPLE_RATE = 44100
BUFFER_SIZE = 512
FADE_OUT_MS = 1000  # Your 1-second sustain

