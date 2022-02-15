from os import listdir
from os.path import join


class Corpus:
    def __init__(self, path_to_dir):
        self.path = path_to_dir

    def emails(self):
        files = listdir(self.path)
        for file in files:
            if not file.startswith('!'):
                with open(join(self.path, file), 'r', encoding= 'utf-8') as f:
                    yield (file, f.read())



