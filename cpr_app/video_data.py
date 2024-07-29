import cv2
class VideoData():
    def __init__(self,place):
        self._name = "output_data"
        self._place = place
        cap = cv2.VideoCapture(place)
        fps = cap.get(cv2.CAP_PROP_FPS)
        #fps = 119.88
        self._fps = fps
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        time = int(frame_count) / int(fps)
        self._time  = int(time)
        
        
        print("fps"+str(fps))
        print(str(type(fps)))
        print("frame count"+str(frame_count))
        print(str(type(frame_count)))
        print("time"+str(time))


    @property
    def time(self):
        return self._time
    @property
    def place(self):
        return self._place
    @property
    def name(self):
        return self._name
    @property
    def fps(self):
        return self._fps
    



