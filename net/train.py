# coding: utf-8

import datetime
import os

import numpy as np
from keras.constraints import maxnorm
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.models import Sequential
from keras.optimizers import SGD
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

img_width = 48
img_height = 48
epochs = 50
seed = 128
num_train = 2648
num_valid = 331
np.random.seed(seed)
img_size = (img_height, img_width)
data_dir = 'data'
train_dir = '{}/train/'.format(data_dir)
validation_dir = '{}/validation/'.format(data_dir)


def load_img(path):
    img = image.load_img(path, target_size=img_size)
    x = image.img_to_array(img)
    return x


def get_classes_from_train_dir():
    d = train_dir
    return sorted([o for o in os.listdir(d) if os.path.isdir(os.path.join(d, o))])


def train():
    classes = get_classes_from_train_dir()
    num_classes = len(classes)
    model = Sequential()
    model.add(
        Convolution2D(48, 3, 3, input_shape=(3, img_height, img_width), border_mode='same', activation='relu',
                      W_constraint=maxnorm(3)))
    model.add(Dropout(0.2))
    model.add(Convolution2D(48, 3, 3, activation='relu', border_mode='same', W_constraint=maxnorm(3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(96, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(96, 3, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    lrate = 0.009
    decay = lrate / epochs
    sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    # this is the augmentation configuration we will use for testing:
    # only rescaling
    test_datagen = ImageDataGenerator(rescale=1. / 255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        classes=classes)

    validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=img_size,
        classes=classes)

    model.fit_generator(
        train_generator,
        samples_per_epoch=num_train,
        nb_epoch=epochs,
        validation_data=validation_generator,
        nb_val_samples=num_valid)

    model.save("model_3classes_aug.h5")

print('Started: ' + str(datetime.datetime.now()))
train()
print('Finished: ' + str(datetime.datetime.now()))
