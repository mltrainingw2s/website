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
from ipware import get_client_ip
import random
import datetime

nowtime = datetime.datetime.now()

# Create your views here.
def index(request):
    ip = get_client_ip(request)
    url = 'https://api.ipfind.com/?ip=' + ip
    response = urllib.request.urlopen(url)
    data1 = json.loads(response.read())
    longitude=data1["longitude"]
    latitude=data1["latitude"]
    print("index: ",ip,longitude,latitude,nowtime)
    return render(request,"index.html")

def imgdetect(request):
    ip = get_client_ip(request)
    url = 'https://api.ipfind.com/?ip=' + ip
    response = urllib.request.urlopen(url)
    data1 = json.loads(response.read())
    longitude=data1["longitude"]
    latitude=data1["latitude"]
    print("imagesout: ",ip,longitude,latitude,nowtime)
    if request.method == "POST" and 'image' in request.FILES:
        # print("enter-------------")
        ip = get_client_ip(request)
        print("images: ",ip)
        imgs = request.FILES['image']
        # fss = FileSystemStorage()
        # fie = fss.save(imgs.name, imgs)
        # print(fie,"this is file")
        # print("its coming",imgs)
        im =Image.open(imgs)
        im.save('/home/ubuntu/img/'+str(imgs))
        # im.show()
        # print(str(BASE_DIR)) 
        # print("sdfsfsfsd")
        input_image = cv2.imread('/home/ubuntu/img/'+str(imgs))
        # print("aaaaa",input_image)
        frame_flip = input_image
        # print(input_image,"input image")
        emotion_detector = FER(mtcnn=True)
        result = emotion_detector.detect_emotions(frame_flip)
        # print(result,"result")
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
                emotion_name, score = emotion_detector.top_emotion(frame_flip)
                a=list(emotions.items())
                emotion_name=a[3][0]
                # print(emotion_name)
                score=a[3][1]
                # print("score",score)
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
                # print("smile",smile_percent)
                # print(smile_percent,"this is the smile percentage")
                cv2.putText(frame_flip,emotion_score,
                        (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                        cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
                #Save the result in new image file
                cv2.imwrite(str(BASE_DIR)+"/static/detectimg/"+str(imgs),frame_flip)
            # print(list_smile,"smile percentaages ")
            strings=" "
            commas=","
            for i in list_smile:
                # print(i)
                strings += str(i)
                strings += commas
            # print(strings)
            save_test = Ml_Image.objects.create(image_upload = str(imgs),smile_percentage = content,image_type = 1)
            get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
            # print("get",get_image)
            return render(request,"imagedetect.html",{'detect_img':imgs,"smile_percent":strings,"content":data,"gallery":get_image,"funny":funny,"pop":pop,"buttons":"block"})
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
            # print("This is the self b",b)
            frame = camera.get_frame(b)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            break

    #Method for laptop camera
    def snap_feed(self,request):
        b=self.a
        # print(self.a,"sdafsdfasd")
        return StreamingHttpResponse(self.gen_image(SnapCamera()),
                        #video type
                        content_type='multipart/x-mixed-replace; boundary=frame')

    def snapdetect(self,request):
        # print("the body request",request.body.decode('utf-8'))
        # self.d= request.POST.get('buton')
        # print("this is the button value",self.a)
        # if self.d=="q":
        #     print("came here")
        #     self.a = self.d
        ip = get_client_ip(request)
        url = 'https://api.ipfind.com/?ip=' + ip
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]
        print("snaaps: ",ip,longitude,latitude,nowtime)
        if request.method == "POST":
            names=request.POST.get("test")
            s = names.split(',')
            # print("s",s)
            img_name_len = 15
            save_name_len = 10
            characters = "abcdefghijklm1234567890nopqrstuvwxyz"
            random_char = [random.choice(characters) for i in range(img_name_len)]
            ran_char = [random.choice(characters) for i in range(save_name_len)]
            joinsran = "".join(random_char)
            saveran = "".join(ran_char)
            firstimg = str(joinsran)
            saveimgs = str(saveran)
            import base64
            with open("/home/ubuntu/img/"+firstimg+".jpg", "wb") as fh:
                fh.write(base64.b64decode(s[1]))
            input_image1 = cv2.imread("/home/ubuntu/img/"+firstimg+".jpg")
            picture = Image.open('/home/ubuntu/img/'+firstimg+'.jpg').convert('L')
            # print("pcc",picture)
            picture = picture.save("/home/ubuntu/img/"+saveimgs+".jpg")
            # im.save('C:/Users/VC/Downloads/'+str(imgs))
            input_image = cv2.imread('/home/ubuntu/img/'+saveimgs+'.jpg')
            # print("test",input_image.shape)
            # print("aaaaa",input_image.shape)
            # print(input_image,"input image")
            emotion_detector = FER(mtcnn=True)
            # print("emo",emotion_detector)
            result = emotion_detector.detect_emotions(input_image)
            # print(result,"result")
            pop = 0
            if result != []:
                list_smile = []
                for i in result:
                    bounding_box = i["box"]
                    emotions = i["emotions"]
                    cv2.rectangle(input_image1,(
                    bounding_box[0], bounding_box[1]),(
                    bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                                (0, 155, 255), 2,)
                    max_emotions=max(i['emotions'], key= lambda x: i['emotions'][x])
                    all_values = emotions.values()
                    max_value = max(all_values)
                    # print(max_emotions)
                    # print(max_value)
                    emotion_name, score = emotion_detector.top_emotion(input_image1)
                    a=list(emotions.items())
                    emotion_name=a[3][0]
                    # print(emotion_name)
                    score=a[3][1]
                    # print("score",score)
                    emotion_name="Smile"
                    color = (255,50,50)
                    content = score *100
                    # print("conte",content)
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
                    # print("smile",smile_percent)
                    # print(smile_percent,"this is the smile percentage")
                    cv2.putText(input_image1,emotion_score,
                            (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                            cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
                    #Save the result in new image file
                    cv2.imwrite(str(BASE_DIR)+"/static/detectimg/"+saveimgs+'.jpg',input_image1)
                # print(list_smile,"smile percentaages ")
                strings=" "
                commas=","
                for i in list_smile:
                    print(i)
                    strings += str(i)
                    strings += commas
                # print(strings)
                save_test = Ml_Image.objects.create(image_upload = str(saveimgs+'.jpg'),smile_percentage = content,image_type = 1)
                get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
                # print("get",get_image)
                return render(request,"snapcam.html",{'detect_img':str(saveimgs+'.jpg'),"smile_percent":strings,"content":data,"gallery":get_image,"funny":funny,"pop":pop,"buttons":"block"})
            else:
                pop = 1
                get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
                return render(request,"snapcam.html",{'detect_img':"5.png","smile_percent":"80%","gallery":get_image,"pop":pop,"buttons":"none"})
        else:
            return render(request,"snapcam.html",{'detect_img':"5.png","smile_percent":"80%","buttons":"none"})

#Method for phone camera
# def webcam_feed(request):
# 	return StreamingHttpResponse(gen(IPWebCam()),
#                     #video type
# 					content_type='multipart/x-mixed-replace; boundary=frame')