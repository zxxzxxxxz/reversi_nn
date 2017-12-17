import os
import json
import numpy as np
from keras import backend as K
from keras.callbacks import EarlyStopping
from keras.layers import Activation, BatchNormalization, Conv2D, Dense, Dropout, Flatten, InputLayer, MaxPooling2D
from keras.models import Sequential, model_from_json, load_model
from keras.optimizers import Adam, RMSprop, SGD
from keras.losses import categorical_crossentropy, mean_squared_error
from keras.utils import to_categorical, plot_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

config = json.load(open("config.json", "r"))


class Train:
    x_train = None  # type: np.ndarray
    x_test = None  # type: np.ndarray
    y_train = None  # type: np.ndarray
    y_test = None  # type: np.ndarray

    model = None

    def plot(self, epochs, history):
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        plt.plot(range(epochs), loss, marker='.', label='loss')
        plt.plot(range(20), val_loss, marker='.', label='val_loss')
        plt.legend(loc='best', fontsize=10)
        plt.grid()
        plt.xlabel('epoch')
        plt.ylabel('loss')
        plt.show()

        acc = history.history['acc']
        val_acc = history.history['val_acc']

        # accuracyのグラフ
        plt.plot(range(20), acc, marker='.', label='acc')
        plt.plot(range(20), val_acc, marker='.', label='val_acc')
        plt.legend(loc='best', fontsize=10)
        plt.grid()
        plt.xlabel('epoch')
        plt.ylabel('acc')
        plt.show()

    def make_model(self):
        model = Sequential()
        model.add(InputLayer(input_shape=(self.x_train.shape[1:])))
        model.add(Conv2D(192, (5, 5), padding='same'))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        for i in range(2):
            model.add(Conv2D(192, (3, 3), padding='same'))
            model.add(Activation('relu'))
            model.add(BatchNormalization())
        model.add(Conv2D(1, (1, 1), padding='same', use_bias=True))
        for i in range(5):
            model.add(Activation('relu'))
            model.add(BatchNormalization())
        model.add(Activation('softmax'))
        model.add(Flatten())

        self.model = model

    def load_model(self):
        self.model = load_model(config["model_path"])

    def save_model(self):
        self.model.save(config["model_path"])

    def save_png(self):
        plot_model(self.model, to_file=config["model_image_path"], show_shapes=True)

    def train(self):
        model = self.model

        batch_size = 128
        epochs = 100

        model.compile(loss='mean_squared_error', optimizer="adam", metrics=['accuracy'])

        history = model.fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs, verbose=0)

        score = model.evaluate(self.x_test, self.y_test, verbose=1)

        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

        self.model= model

    def __init__(self, field_size: np.ndarray):
        # フィールドの要素数
        num_classes = field_size[0] * field_size[1]

        self.x_train = np.load(config["x_train_path"])
        self.y_train = np.load(config["y_train_path"])
        self.x_test = np.load(config["x_test_path"])
        self.y_test = np.load(config["y_test_path"])


field_size = np.array([8, 8])

train = Train(field_size)
if os.path.exists(config["model_path"]):
    print("load model")
    train.load_model()
else:
    print("make model")
    train.make_model()
    train.save_png()
train.train()
train.save_model()
