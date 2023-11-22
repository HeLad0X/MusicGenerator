import sys
import os
import music21 as m21
import json
import keras
import numpy as np

sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'\\rnn_model')

from backend.config import (
    get_train_data_path, 
    ACCEPTABLE_DURATIONS, 
    SEQUENCE_LENGTH, 
    get_single_file_path,
    get_multiple_file_path,
    get_mapping_path,
    set_output
)

    
def get_file_path_list():
    data_dir = get_train_data_path()
    filenames = []

    for (dir_path, dir_names, file_names) in os.walk(data_dir):
        file_names = [dir_path + '\\' + file for file in file_names if file[-3:] == 'krn']
        filenames.extend(file_names)

    return filenames

def has_acceptable_duration(song):
    for note in song.flat.notesAndRests:
        if note.duration.quarterLength not in ACCEPTABLE_DURATIONS:
            return False

    return True


def transpose_song(song):
    # Get key from the song
    parts = song.getElementsByClass(m21.stream.Part)
    measures_part_0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = None
    
    try:
        key = measures_part_0[0][4]

    except IndexError:
        return None, False

    # Estimate key using music21
    if not isinstance(key, m21.key.Key):
        key = song.analyze('key')

    if key.mode == 'major':
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch('C'))
    elif key.mode == 'minor':
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch('A'))

    transposed_song = song.transpose(interval)

    return transposed_song, True


def encode_song(song, time_step = 0.25):
    encoded_song = []
    for event in song.flat.notesAndRests:
        # handle notes
        if isinstance(event, m21.note.Note):
            symbol = event.pitch.midi
        
        # Handle rests
        elif isinstance(event, m21.note.Rest):
            symbol = 'r'
        
        steps = int(event.duration.quarterLength / time_step)
        for step in range(steps):
            if step == 0:
                encoded_song.append(symbol)
            else:
                encoded_song.append('_')

    # cast the encoded song to string
    encoded_song_str = ' '.join(map(str,encoded_song))

    return encoded_song_str


def load(file_path):
    with open(file_path, 'r') as f:
        song = f.read()

    return song


def create_single_file_dataset(project_id):
    print('-----------Creating single file data-------------------')
    multiple_file_path = get_multiple_file_path(project_id)
    new_song_delimiter = '/ ' * SEQUENCE_LENGTH

    songs = ""

    for path, _, files in os.walk(multiple_file_path):
        for file in files:
            file_path = os.path.join(path,file)
            song = load(file_path)
            songs = songs + song + ' ' + new_song_delimiter

    songs = songs[:-1]
    
    single_file_path = get_single_file_path(project_id)

    with open(single_file_path,'w') as fp:
        fp.write(songs)

    return songs


def save_encoded_songs_to_path(song,i, project_id):
    save_data_folder = get_multiple_file_path(project_id=project_id)

    save_path = os.path.join(save_data_folder,str(i))
    with open(save_path, 'w') as fp:
        fp.write(song)



def create_mapping(songs,project_id):
    print('------------Creating mapping-----------------')
    mappings = {}

    songs = songs.split()
    vocabulary = list(set(songs))


    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i

    mapping_path = get_mapping_path(project_id)
    with open(mapping_path,'w') as fp:
        json.dump(mappings,fp,indent=4)

    with open(mapping_path,'r') as f:
        mappings = json.load(f)



def convert_song_to_int(songs,project_id):
    print('---------Conoverting Song to int--------------')

    int_songs = []

    # load the mapping
    mapping_path = get_mapping_path(project_id)

    with open(mapping_path,'r') as f:
        mappings = json.load(f)

    set_output(len(mappings))
    # cast songs string to list
    songs = songs.split()


    # map songs to int
    for symbol in songs:
        int_songs.append(mappings[symbol])

    return int_songs


def generating_training_sequences(project_id):
    print('----------generating training sequence------------')
    single_file_path = get_single_file_path(project_id)
    
    songs = load(single_file_path)
    int_songs = convert_song_to_int(songs=songs,project_id=project_id)

    inputs = []
    targets = []

    num_sequences = len(int_songs) - SEQUENCE_LENGTH
    for i in range(num_sequences):
        try:
            inputs.append(int_songs[i:i+SEQUENCE_LENGTH])
            targets.append(int_songs[i+SEQUENCE_LENGTH])
        except IndexError:
            break

    vocabulary_size = len(set(int_songs))
    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)

    return inputs, targets




def begin_preprocess(project_id=0):
    file_path_list = get_file_path_list()
    print('Total files:',len(file_path_list))
    for i, file in enumerate(file_path_list):
        song = m21.converter.parse(file)
        if has_acceptable_duration(song):
            transposed_song, status = transpose_song(song)
            if not status: continue
            encoded_song = encode_song(transposed_song)
            save_encoded_songs_to_path(encoded_song,i,project_id)
        
        if i%100 == 0:
            print(f'{i} data done')

    songs = create_single_file_dataset(project_id=project_id)
    songs = load(get_single_file_path(project_id=project_id))
    create_mapping(songs=songs,project_id=project_id)
    inputs, targets = generating_training_sequences(project_id=project_id)
    return inputs,targets
