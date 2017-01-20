from keras.models import load_model
from keras.preprocessing import image
import numpy as np


def load_img(path):
    img = image.load_img(path, target_size=img_size)
    x = image.img_to_array(img)
    return x


def predict(url):
    global model
    img = load_img(url)
    img = np.expand_dims(img, axis=0)
    preds = model.predict(img)
    val, idx = max((val, idx) for (idx, val) in enumerate(preds[0]))
    print('For ' + url + ' predicted ' + classes[idx])
    return classes[idx]

img_size = (48, 48)
classes = ['cheese', 'milk', 'tomato']
model = load_model("3classes_with_augmentation.h5")