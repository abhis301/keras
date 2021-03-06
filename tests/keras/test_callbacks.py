import pytest
import os
import numpy as np
np.random.seed(1337)

from keras import callbacks
from keras.models import Graph, Sequential
from keras.layers.core import Dense
from keras.utils.test_utils import get_test_data
from keras import backend as K
from keras.utils import np_utils

input_dim = 2
nb_hidden = 4
nb_class = 2
batch_size = 5
train_samples = 20
test_samples = 20


def test_ModelCheckpoint():
    filepath = 'checkpoint.h5'
    (X_train, y_train), (X_test, y_test) = get_test_data(nb_train=train_samples,
                                                         nb_test=test_samples,
                                                         input_shape=(input_dim,),
                                                         classification=True,
                                                         nb_class=nb_class)
    y_test = np_utils.to_categorical(y_test)
    y_train = np_utils.to_categorical(y_train)
    # case 1
    monitor = 'val_loss'
    save_best_only = False
    mode = 'auto'

    model = Sequential()
    model.add(Dense(nb_hidden, input_dim=input_dim, activation='relu'))
    model.add(Dense(nb_class, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    cbks = [callbacks.ModelCheckpoint(filepath, monitor=monitor,
                                      save_best_only=save_best_only, mode=mode)]
    model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
              validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=1)
    assert os.path.exists(filepath)
    os.remove(filepath)

    # case 2
    mode = 'min'
    cbks = [callbacks.ModelCheckpoint(filepath, monitor=monitor,
                                      save_best_only=save_best_only, mode=mode)]
    model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
              validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=1)
    assert os.path.exists(filepath)
    os.remove(filepath)

    # case 3
    mode = 'max'
    monitor = 'val_acc'
    cbks = [callbacks.ModelCheckpoint(filepath, monitor=monitor,
                                      save_best_only=save_best_only, mode=mode)]
    model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
              validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=1)
    assert os.path.exists(filepath)
    os.remove(filepath)

    # case 4
    save_best_only = True
    cbks = [callbacks.ModelCheckpoint(filepath, monitor=monitor,
                                      save_best_only=save_best_only, mode=mode)]
    model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
              validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=1)
    assert os.path.exists(filepath)
    os.remove(filepath)


def test_EarlyStopping():
    (X_train, y_train), (X_test, y_test) = get_test_data(nb_train=train_samples,
                                                         nb_test=test_samples,
                                                         input_shape=(input_dim,),
                                                         classification=True,
                                                         nb_class=nb_class)
    y_test = np_utils.to_categorical(y_test)
    y_train = np_utils.to_categorical(y_train)
    model = Sequential()
    model.add(Dense(nb_hidden, input_dim=input_dim, activation='relu'))
    model.add(Dense(nb_class, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    mode = 'max'
    monitor = 'val_acc'
    patience = 0
    cbks = [callbacks.EarlyStopping(patience=patience, monitor=monitor, mode=mode)]
    history = model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
                        validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=20)

    mode = 'auto'
    monitor = 'val_acc'
    patience = 2
    cbks = [callbacks.EarlyStopping(patience=patience, monitor=monitor, mode=mode)]
    history = model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
                        validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=20)


def test_LearningRateScheduler():
    (X_train, y_train), (X_test, y_test) = get_test_data(nb_train=train_samples,
                                                         nb_test=test_samples,
                                                         input_shape=(input_dim,),
                                                         classification=True,
                                                         nb_class=nb_class)
    y_test = np_utils.to_categorical(y_test)
    y_train = np_utils.to_categorical(y_train)
    model = Sequential()
    model.add(Dense(nb_hidden, input_dim=input_dim, activation='relu'))
    model.add(Dense(nb_class, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='sgd')

    cbks = [callbacks.LearningRateScheduler(lambda x: 1. / (1. + x))]
    model.fit(X_train, y_train, batch_size=batch_size, show_accuracy=True,
              validation_data=(X_test, y_test), callbacks=cbks, nb_epoch=5)
    assert (float(K.get_value(model.optimizer.lr)) - 0.2) < K.epsilon()


if __name__ == '__main__':
    pytest.main([__file__])

