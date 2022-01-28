# from django.shortcuts import render
from django.http import JsonResponse,Http404
from rest_framework import status
import cv2
from fer import FER
from PIL import Image
from .models import Restmlimage,Restmlwebcam
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
from ipware import get_client_ip
import random
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import mlimageserializer
# Create your views here.
class Image_detect(APIView):

    def get(self,request):
        m = Restmlimage.objects.values('id','image_upload','smile_percentage').order_by('-created_at')
        serializer = mlimageserializer(m,many=True)
        print("enters-----",m)
        return Response({'gallery':serializer.data})

    def post(self,request):
        # print("------------------",json.loads(request.body.decode('utf-8')),"----------------")
        if 'data' in request.FILES:
            print("data---------------",request.FILES['data'])
            imgs = request.FILES['data']
            a=str(imgs).split('.')
            imext = ['jpg','jpeg','png','JPEG','JPG','PNG','JFIF','jfif']
            if str(a[1]) in imext:
                im = Image.open(imgs)
                im.save('/home/ubuntu/img/'+str(imgs))
                input_image = cv2.imread('/home/ubuntu/img/'+str(imgs))
                frame_flip = input_image
                emotion_detector = FER(mtcnn=True)
                result = emotion_detector.detect_emotions(frame_flip)
                if result != []:
                    list_smile = []
                    for i in result:
                        bounding_box = i["box"]
                        emotions = i["emotions"]
                        cv2.rectangle(input_image, (
                            bounding_box[0], bounding_box[1]), (
                                          bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                                      (0, 155, 255), 2, )
                        # max_emotions = max(i['emotions'], key=lambda x: i['emotions'][x])
                        all_values = emotions.values()
                        max_value = max(all_values)
                        # print(max_emotions)
                        # print(max_value)
                        emotion_name, score = emotion_detector.top_emotion(frame_flip)
                        a = list(emotions.items())
                        # emotion_name = a[3][0]
                        # print(emotion_name)
                        score = a[3][1]
                        # print("score",score)
                        emotion_name = "Smile"
                        color = (255, 50, 50)
                        content = score * 100
                        if content >= 0 and content <= 20:
                            data = "Smile please,...Smile while you stil have teeth!."
                        elif content >= 21 and content <= 40:
                            data = "Smile ,it increases your face value."
                        elif content >= 41 and content <= 60:
                            data = "Your smile is literally the cutest thing,I have ever seen"
                        elif content >= 61 and content <= 80:
                            data = "Wear a smile on everyday,have a great confidence"
                        else:
                            data = "Your such a happiest and adorable one,don't forget to smile at any situation"
                        emotion_score = "{}: {}".format(emotion_name, "{:.0%}".format(score))
                        smile_percent = "{:.0%}".format(score)
                        list_smile.append(smile_percent)
                        # print("smile",smile_percent)
                        # print(smile_percent,"this is the smile percentage")
                        cv2.putText(frame_flip, emotion_score,
                                    (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2, cv2.LINE_AA, )
                        # Save the result in new image file
                        cv2.imwrite(str(BASE_DIR) + "/static/detectimg/" + str(imgs), frame_flip)
                    # print(list_smile,"smile percentaages ")
                    strings = " "
                    commas = ","
                    for i in list_smile:
                        # print(i)
                        strings += str(i)
                        strings += commas
                    request.data['image_upload'] = str(imgs)
                    request.data['smile_percentage'] = strings
                    # m = Restmlimage.objects.create(image_upload = str(imgs),smile_percentage=int(50))
                    print('datas--------', request.data)
                    serializer = mlimageserializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        context={'msg':serializer.data,'other_msg':data}
                        return Response(context, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"Image doesn't have face or smile on face"},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message':"Upload only images"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg':'please upload image for smile detections'},status=status.HTTP_400_BAD_REQUEST)




