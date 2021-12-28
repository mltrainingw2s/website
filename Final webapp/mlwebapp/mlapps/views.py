from django.shortcuts import render
import cv2
from fer import FER
from PIL import Image
from .models import Ml_Image
from django.core.files.storage import FileSystemStorage
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from PIL import Image
import numpy as np
from mtcnn import MTCNN
import pickle
import json
import tensorflow
from tensorflow.keras.layers import Dense,Input, Flatten, MaxPool2D
from tensorflow.keras.layers import Conv2D,Dropout
from tensorflow.keras import Sequential
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.regularizers import l2,l1
from tensorflow.keras.optimizers import Adam
from imutils.video import VideoStream
import imutils
from django.http.response import StreamingHttpResponse
from mlapps.camera import VideoCamera,SnapCamera
# Create your views here.
def index(request):
    return render(request,"index.html")

def imgdetect(request):
    if request.method == "POST" and 'image' in request.FILES:
        print("enter-------------")
        imgs = request.FILES['image']
        fss = FileSystemStorage()
        fie = fss.save(imgs.name, imgs)
        print(fie,"this is file")
        # print("its coming",imgs)
        # im =Image.open(imgs)
        # im.show()
        print(str(BASE_DIR)) 
        input_image = cv2.imread(str(BASE_DIR)+'/media/'+str(fie))
        # print(input_image,"input image")
        emotion_detector = FER(mtcnn=True)
        result = emotion_detector.detect_emotions(input_image)
        print(result,"result")
        pop = 0
        if result != []:
            list_smile = []
            for i in result:
                bounding_box = i["box"]
                emotions = i["emotions"]
                cv2.rectangle(input_image,(
                bounding_box[0], bounding_box[1]),(
                bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                            (0, 155, 255), 2,)
                max_emotions=max(i['emotions'], key= lambda x: i['emotions'][x])
                all_values = emotions.values()
                max_value = max(all_values)
                # print(max_emotions)
                # print(max_value)
                emotion_name, score = emotion_detector.top_emotion(input_image)
                a=list(emotions.items())
                emotion_name=a[3][0]
                # print(emotion_name)
                score=a[3][1]
                print("score",score)
                emotion_name="Smile"
                color = (255,50,50)
                content = score *100
                if content >= 0  and content <= 20:
                    data = "Smile please,...Smile while you stil have teeth!."
                    funny = "Konjam siringa boss,"
                elif content >= 21 and content <=40:
                    data = "Smile ,it increases your face value."
                    funny = "yena siripu light ah dhaan yetti pakuthu "
                elif content >= 41 and content <=60:
                    data = "Your smile is literally the cutest thing,I have ever seen"
                    funny = "Nalla vela konjamachu sirichiyea"
                elif content >=61 and content <= 80:
                    data = "Wear a smile on everyday,have a great confidence"
                    funny = "Polachi kita, manusan thaan da nee"
                else:
                    data = "Your such a happiest and adorable one,don't forget to smile at any situation"
                    funny = "Appada sirichitan yevolo puyal vanthalum ,evan matum thapichiruvan!"
                emotion_score = "{}: {}".format(emotion_name, "{:.0%}".format(score))
                smile_percent ="{:.0%}".format(score)
                list_smile.append(smile_percent)
                print("smile",smile_percent)
                # print(smile_percent,"this is the smile percentage")
                cv2.putText(input_image,emotion_score,
                        (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                        cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
                #Save the result in new image file
                cv2.imwrite(str(BASE_DIR)+"/static/detectimg/"+str(fie),input_image)
            print(list_smile,"smile percentaages ")
            strings=" "
            commas=","
            for i in list_smile:
                print(i)
                strings += str(i)
                strings += commas
            print(strings)
            save_test = Ml_Image.objects.create(image_upload = str(fie),smile_percentage = content,image_type = 1)
            get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
            print("get",get_image)
            return render(request,"imagedetect.html",{'detect_img':fie,"smile_percent":strings,"content":data,"gallery":get_image,"funny":funny,"pop":pop,"buttons":"block"})
        else:
            pop = 1
            get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
            return render(request,"imagedetect.html",{'detect_img':"5.png","smile_percent":"80%","gallery":get_image,"pop":pop,"buttons":"none"})
    else:
        get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
        return render(request,"imagedetect.html",{'detect_img':"5.png","smile_percent":"80%","gallery":get_image,"buttons":"none"})

def videodetect(request):
    return render(request,"webcamdetect.html")
    
def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Method for laptop camera
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
                    #video type
					content_type='multipart/x-mixed-replace; boundary=frame')

class snaps():
    def __init__(self):
        self.a="0"

    def gen_image(self,camera):
        b = self.a
        # print("cames")
        # print("This is the self b",self.b)
        while True:
            print("This is the self b",b)
            frame = camera.get_frame(b)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            break

    #Method for laptop camera
    def snap_feed(self,request):
        b=self.a
        print(self.a,"sdafsdfasd")
        return StreamingHttpResponse(self.gen_image(SnapCamera()),
                        #video type
                        content_type='multipart/x-mixed-replace; boundary=frame')

    def snapdetect(self,request):
        print("the body request",request.body.decode('utf-8'))
        self.d= request.POST.get('buton')
        print("this is the button value",self.a)
        if self.d=="q":
            print("came here")
            self.a = self.d
        return render(request,"snapcam.html")

#Method for phone camera
# def webcam_feed(request):
# 	return StreamingHttpResponse(gen(IPWebCam()),
#                     #video type
# 					content_type='multipart/x-mixed-replace; boundary=frame')