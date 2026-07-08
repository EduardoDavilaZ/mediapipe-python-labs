import cv2
import mediapipe as mp
import config.config as settings

class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_con=0.7, track_con=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=mode,
            max_num_hands=max_hands,
            min_detection_confidence=detection_con,
            min_tracking_confidence=track_con
        )
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        """Processes the frame and returns a list of hands with their landmarks."""
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        all_hands = []

        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                hand_data = {'landmarks': []}
                for lm in hand_lms.landmark:
                    # Convert normalized coordinates to pixel coordinates
                    cx, cy = int(lm.x * settings.WIDTH), int(lm.y * settings.HEIGHT)
                    hand_data['landmarks'].append((cx, cy, lm.z))
                all_hands.append(hand_data)
        
        return all_hands

    def draw_landmarks(self, frame, hands_data):
        """Draws the skeleton of the hand for visual feedback."""
        if self.results.multi_hand_landmarks:
            for hand_lms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)