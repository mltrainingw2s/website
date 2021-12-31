from imutils.video import VideoStream
import imutils
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings
from fer import Video
from fer import FER
import threading
import time

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)
        print("slef",self.video)
        (self.grabbed, self.frame_flip) = self.video.read()
        print("(self.grabbed, self.frame_flip)",(self.grabbed, self.frame_flip))
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()


    #This function is used in views
    def get_frame(self):
        # detector = MTCNN()
        success, image = self.video.read()
        self.frame_flip = cv2.flip(image, 1)
        # detector = FER()
        # a=detector.detect_emotions(frame_flip)
        emotion_detector = FER(mtcnn=True)
        result = emotion_detector.detect_emotions(self.frame_flip)
        print(result,"result")
        for i in result:
            bounding_box = i["box"]
            emotions = i["emotions"]
            cv2.rectangle(self.frame_flip,(
            bounding_box[0], bounding_box[1]),(
            bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                        (0, 155, 255), 2,)
            max_emotions=max(i['emotions'], key= lambda x: i['emotions'][x])
            all_values = emotions.values()
            max_value = max(all_values)
            # print(max_emotions)
            # print(max_value)
            emotion_name, score = emotion_detector.top_emotion(self.frame_flip)
            a=list(emotions.items())
            emotion_name=a[3][0]
            # print(emotion_name)
            score=a[3][1]
            print("score",score)
            emotion_name="Smile"
            color = (255,50,50)
            content = score *100
            emotion_score = "{}: {}".format(emotion_name, "{:.0%}".format(score))
            smile_percent ="{:.0%}".format(score)
            print("smile",smile_percent)
            # print(smile_percent,"this is the smile percentage")
            cv2.putText(self.frame_flip,emotion_score,
                    (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                    cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
        imgs =self.frame_flip
        self.ret, self.jpeg = cv2.imencode('.jpg', imgs)
        return self.jpeg.tobytes()
    
    def update(self):
        while True:
            (self.grabbed,self.frame_flip) = self.video.read()
            return self.jpeg.tobytes()


class SnapCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame_flip) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()


    #This function is used in views
    def get_frame(self,data):
        # detector = MTCNN()
        self.data = data
        print("datas",self.data)
        success, image = self.video.read()
        self.frame_flip = cv2.flip(image, 1)
        # detector = FER()
        # a=detector.detect_emotions(frame_flip)
        # emotion_detector = FER(mtcnn=True)
        # result = emotion_detector.detect_emotions(self.frame_flip)
        # print(result,"result")
        # for i in result:
        #     bounding_box = i["box"]
        #     emotions = i["emotions"]
        #     cv2.rectangle(self.frame_flip,(
        #     bounding_box[0], bounding_box[1]),(
        #     bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
        #                 (0, 155, 255), 2,)
        #     max_emotions=max(i['emotions'], key= lambda x: i['emotions'][x])
        #     all_values = emotions.values()
        #     max_value = max(all_values)
        #     # print(max_emotions)
        #     # print(max_value)
        #     emotion_name, score = emotion_detector.top_emotion(self.frame_flip)
        #     a=list(emotions.items())
        #     emotion_name=a[3][0]
        #     # print(emotion_name)
        #     score=a[3][1]
        #     print("score",score)
        #     emotion_name="Smile"
        #     color = (255,50,50)
        #     content = score *100
        #     emotion_score = "{}: {}".format(emotion_name, "{:.0%}".format(score))
        #     smile_percent ="{:.0%}".format(score)
        #     print("smile",smile_percent)
        #     # print(smile_percent,"this is the smile percentage")
        #     cv2.putText(self.frame_flip,emotion_score,
        #             (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
        #             cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
        imgs =self.frame_flip
        self.ret, self.jpeg = cv2.imencode('.jpg', imgs)
        return self.jpeg.tobytes()
    
    def update(self):
        while True:
            (self.grabbed,self.frame_flip) = self.video.read()
            return self.jpeg.tobytes()
# class IPWebCam(object):
#     def __init__(self):
#         self.url = "http://192.168.1.178:8080/shot.jpg"


#     def __del__(self):
#         cv2.destroyAllWindows()

#     def get_frame(self):
#         imgResp = urllib.request.urlopen(self.url)
#         imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
#         img = cv2.imdecode(imgNp, -1)
#         img =cv2.resize(img, (640, 480))
#         frame_flip = cv2.flip(img, 1)
#         ret, jpeg = cv2.imencode('.jpg', frame_flip)
#         return jpeg.tobytes()