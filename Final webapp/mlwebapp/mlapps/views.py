from django.shortcuts import render
import cv2
from fer import FER
from PIL import Image
from .models import Ml_Image
from django.core.files.storage import FileSystemStorage
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
import json
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
            print("smile",smile_percent)
            # print(smile_percent,"this is the smile percentage")
            cv2.putText(input_image,emotion_score,
                    (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                    cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
            #Save the result in new image file
            cv2.imwrite(str(BASE_DIR)+"/static/detectimg/"+str(fie),input_image)
            save_test = Ml_Image.objects.create(image_upload = str(fie),smile_percentage = content,image_type = 1)
            get_image = Ml_Image.objects.values('image_upload','image_type','smile_percentage').order_by('-created_at')
            print("get",get_image)
        return render(request,"imagedetect.html",{'detect_img':fie,"smile_percent":smile_percent,"content":data,"gallery":get_image,"funny":funny})
    else:
        return render(request,"imagedetect.html",{'detect_img':"5.png","smile_percent":"80%"})

def videodetect(request):
    return render(request,"webcamdetect.html")

