import os
import json
import numpy as np

from funcs import GetTestCoord

config = json.load(open("config.json", "r"))

# データセット読み込み
x_train = np.load(config["x_train_path"])
y_train = np.load(config["y_train_path"])

y_test = []

for i in range(len(y_train)):
    print(str(i + 1) + "/" + str(len(y_train)))
    y_test.append(GetTestCoord(y_train[i]))

np.save(config["x_test_path"], x_train)
np.save(config["y_test_path"], y_test)