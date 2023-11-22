import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\rnn_model')

import keras
from backend.rnn_model.preprocess import generating_training_sequences,begin_preprocess
from backend.config import (get_model_path, 
                    OUTPUT_UNITS,
                    LOSS,
                    LEARNING_RATE,
                    NUM_UNITS,
                    EPOCHS,
                    BATCH_SIZE)




def build_model():
    output_units = OUTPUT_UNITS()
    num_units = NUM_UNITS
    loss = LOSS
    learning_rate = LEARNING_RATE

    inputs = keras.layers.Input(shape=(None,output_units))
    x = keras.layers.LSTM(num_units[0])(inputs)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units,activation='softmax')(x)

    model = keras.Model(inputs,output)

    model.compile(loss=loss, 
                  optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                  metrics=['accuracy'])
    
    print(model.summary())

    return model


def run_rnn(project_id):
    inputs, targets = begin_preprocess(project_id)

    model = build_model()
    
    model.fit(inputs, targets, epochs = EPOCHS, batch_size = BATCH_SIZE)

    save_model_path = get_model_path(project_id)
    model.save(save_model_path)

run_rnn(1)