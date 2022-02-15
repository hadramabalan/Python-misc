from corpus import Corpus
from utils import read_classification_from_file


class TrainingCorpus(Corpus):
    def get_class(self, fname):
        truth_dict = read_classification_from_file(self.path + '/!truth.txt')
        return truth_dict[fname]

    def is_ham(self, fname):
        if self.get_class(fname) == "OK":
            return True
        else:
            return False

    def is_spam(self, fname):
        if self.get_class(fname) == "SPAM":
            return True
        else:
            return False
