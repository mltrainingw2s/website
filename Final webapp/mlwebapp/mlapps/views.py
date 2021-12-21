from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Image
from django.core.files.storage import default_storage
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import cv2



# Create your views here.
# @api_view(['GET', 'POST'])
## viewing all image uploaded 
def index(request):
    return render(request,"index.html",)

### image_type -1 normal upload
### image_type -2 webcam upload
@api_view(['GET', 'POST'])
def imgdetect(request):
    # print("sasa",request.FILES['image'])
    # if request.method == "POST" and 'image' in request.FILES:
        # imgs = request.FILES['image']
    imgs = 'C:/Users/VC/Downloads/depositphotos_12196477-stock-photo-smiling-men-isolated-on-the.jpg'
    input_image = cv2.imread(imgs)
    print("saa",input_image)
    emotion_detector = FER(mtcnn=True)
    result = emotion_detector.detect_emotions(input_image)
    print(result)
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
        print(max_emotions)
        print(max_value)
        emotion_name, score = emotion_detector.top_emotion(input_image)
        a=list(emotions.items())
        emotion_name=a[3][0]
        print(emotion_name)
        score=a[3][1]
        emotion_name="Smile"
        color = (255,50,50)
        emotion_score = "{}: {}".format(emotion_name, "{:.0%}".format(score))
        cv2.putText(input_image,emotion_score,
                (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + 3 * 0),
                cv2.FONT_HERSHEY_SIMPLEX,0.75,color,2,cv2.LINE_AA,)
        #Save the result in new image file
        cv2.imwrite("D:\\emotion.jpg", input_image)
        print("BASE_DIR",BASE_DIR)
        file = request.FILES["image"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.size(file_name)
        print("file",file_url)
        save_test = Image.objects.create(image_upload = file,smile_percentage = 1,image_type = 1)
        get_image = Image.objects.values_list('image_upload','image_type','smile_percentage')
        print("image",get_image)
    return(request,"imagedetect.html")
    # else:
    #     return render(request,"imagedetect.html")

def videodetect(request):
    if request.method == "POST":
        print("BASE_DIR",BASE_DIR)
        file = request.FILES["image"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.size(file_name)
        print("file",file_url)
        save_test = Image.objects.create(image_upload = "anb",smile_percentage = 1,image_type = 2)
    return render(request,"webcamdetect.html")