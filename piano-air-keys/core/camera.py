import cv2

class Camera:
    def __init__(self, index=0, width=640, height=480):
        self.capture = cv2.VideoCapture(index)
        
        # Force resolution
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        
        if not self.capture.isOpened():
            raise ValueError(f"Error: Could not open video device with index {index}.")

    def get_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return None
        return cv2.flip(frame, 1)

    def release(self):
        self.capture.release()
        cv2.destroyAllWindows()