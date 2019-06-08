import os, os.path
import errno
import json

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def load_json(path):
    data = {}
    try:
        with open(path) as f:
            data = json.load(f)
        print(f'{path} successfully loaded')
    except:
        print('Could not load json')
    return data

def save_json(path, data):
    mkdir_p(os.path.dirname(path))
    with open(path, 'w') as f:
        json.dump(data, f)
