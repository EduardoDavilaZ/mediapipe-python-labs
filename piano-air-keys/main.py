import cv2
from core.camera import Camera
from core.detector import HandDetector
from piano.keyboard import Keyboard
from piano.audio_engine import AudioEngine
import config.config as settings

def main():
    camera = Camera(width=settings.WIDTH, height=settings.HEIGHT)
    detector = HandDetector()
    engine = AudioEngine()
    piano_keyboard = Keyboard(octaves=[4, 5])
    
    last_notes = set()

    while True:
        frame = camera.get_frame()
        if frame is None: break

        hands_data = detector.find_hands(frame)
        current_active_notes = set()
        finger_tips = [4, 8, 12, 16, 20]

        for hand in hands_data:
            lms = hand['landmarks']
            for tip in finger_tips:
                note = piano_keyboard.check_collision(lms, tip)
                if note:
                    current_active_notes.add(note)

        new_notes = current_frame_notes = current_active_notes - last_notes
        for note in new_notes:
            print(f"Tocando: {note}")
            engine.play(note)

        last_notes = current_active_notes

        # draw
        piano_keyboard.draw(frame, current_active_notes)
        detector.draw_landmarks(frame, hands_data)

        cv2.imshow("Piano Gesture Pro", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    camera.release()

if __name__ == "__main__":
    main()