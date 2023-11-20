import os
import pathlib
import tensorflow as tf
import sys

sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\rnn_model')

from config import get_train_data_path

def start_midi_file_download():
  data_dir = get_train_data_path()
  if not data_dir.exists():
    tf.keras.utils.get_file(
        'maestro-v2.0.0-midi.zip',
        origin='https://storage.googleapis.com/magentadata/datasets/maestro/v2.0.0/maestro-v2.0.0-midi.zip',
        extract=True,
        cache_dir='.', cache_subdir='data',
    )