from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
import tensorflow as tf
import tensorflow_hub as hub
from keras.models import load_model
from keras.applications.mobilenet_v2 import preprocess_input
from skimage.transform import resize
import numpy as np
from imageio import imread

import os
from .forms import *
from .models import *

DIR = os.path.dirname(__file__)

data = np.empty((40, 224, 224, 3))

'''
    tomato model has 7 classes
    healthy - 0
    bacterial_spot - 1
    curl - 2
    early blight - 3
    leaf mold - 4
    spider mite - 5
    sepetoria leaf spot - 6

'''
tomato_model_path = os.path.join(DIR, 'img_models/tomato.h5')

# potato model has 2 classes
# early_blight - 0
# late blight - 1
potato_model_path = os.path.join(DIR, 'img_models/potato.h5')

'''
    pepper model has two classes
    pepper healthy - 0
    pepper_bacterial_spot - 1
'''
pepper_model_path = os.path.join(DIR, 'img_models/pepper.h5')


model = load_model(tomato_model_path, custom_objects={
                   'KerasLayer': hub.KerasLayer})

filename = DIR+'/leaf_mold.5.jpg'


def index(request):
    # for i in range(0,1):
    #     img = imread(filename)
    #     img = preprocess_input(img)
    #     img = resize(img, output_shape=(224,224))
    #     data[i] = img
    # predictions = model.predict(data)
    # class_name = np.argmax(predictions[:6], axis=1)
    if request.method == 'POST':
        # if 'potAto' in request.POST:
        form = InputForm(request.POST, request.FILES)
        tomatoForm = TomatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = Pepper()
    context = {
        'form': form
    }
    return render(request, 'index.html', context)


def pepper(request):
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('result')
    else:
        form = Pepper()
    context = {
        'form': form
    }
    return render(request, 'pepper.html', context)


def tomato(request):
    return render(request, 'tomato.html')


def potato(request):
    return render(request, 'potato.html')


def result(request):
    imgs = Pepper.objects.all().order_by('-created_on')[:1]
    # img_src = 'media/' + 1
    class_name = ''
    classname = ''

    for image in imgs:
        # print (imgs[i])
        for i in range(1):
            img = imread('media/' + image.image.name)
            img = preprocess_input(img)
            img = resize(img, output_shape=(224, 224))
            data[i] = img
        predictions = model.predict(data)
        class_name = np.argmax(predictions[:1], axis=1)
        if class_name[0] == 0:
            classname = 'healthy'
        elif class_name[0] == 1:
            classname = 'bacterial'
        elif class_name[0] == 2:
            classname = 'curl'
        elif class_name[0] == 3:
            classname = 'early blight'
        elif class_name[0] == 4:
            classname = 'leaf mold'
        elif class_name[0] == 5:
            classname = 'spider mite'
        else:
            classname = 'sepetoria'
    context = {
        'img': imgs,
        'classname': classname
    }
    print(class_name[0])
    # print(imgs)

    return render(request, 'result.html', context)
