from corpus import Corpus
from trainingcorpus import TrainingCorpus
from utils import word_freq_in_file
from collections import Counter
import math

class MyFilter:
    """Simple naive Bayes filter"""
    def __init__(self):
        self.mail_total = 0

        # set during training
        self.pSpam = 0  # percentage of spam mails
        self.pHam = 0   # percentage of ham mails

        # increased by process_spam_mail (during training)
        self.spam_mail_total = 0
        self.spam_word_count = 0  # total number of words in spam mails
        self.spam_word_freq = Counter()  # how many times each word was used in spams

        # increased by process_ham_mail (during training)
        self.ham_mail_total = 0
        self.ham_word_count = 0  # total number of words in ham mails
        self.ham_word_freq = Counter()   # how many times each word was used in hams

    def write_to_file(self, dic, path):
        text = ""
        for i in dic:
            text += i + " " + dic[i] + "\n"

        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)

    def process_ham_mail(self, file):
        self.ham_mail_total += 1
        self.mail_total += 1
        temp_result = word_freq_in_file(file)  # counter of frequencies and count of total words in
        self.ham_word_count += temp_result[1]
        self.ham_word_freq.update(temp_result[0])

    def process_spam_mail(self, file):
        self.spam_mail_total += 1
        self.mail_total += 1
        temp_result = word_freq_in_file(file) # counter of frequencies and count of total words
        self.spam_word_count += temp_result[1]
        self.spam_word_freq.update(temp_result[0])

    def train(self, path):
        corpus = TrainingCorpus(path)
        for email in corpus.emails():
            if corpus.is_ham(email[0]):
                self.process_ham_mail(email[1])
            else:
                self.process_spam_mail(email[1])
        self.pSpam = self.spam_mail_total / self.mail_total
        self.pHam = self.ham_mail_total / self.mail_total




    def test(self, path):
        corpus = Corpus(path)
        dic = {}
        for email in corpus.emails():
            title = email[0]
            counter = word_freq_in_file(email[1])[0]
            pSpam, pHam = math.exp(self.pSpam), math.exp(self.pHam)
            for word in counter:
                if self.spam_word_freq[str(word)] != 0:
                    pSpam += math.exp(self.spam_word_freq[word] / self.spam_word_count)
                if self.ham_word_freq[str(word)] != 0:
                    pHam += math.exp(self.ham_word_freq[word] / self.ham_word_count)

            if pSpam > pHam:
                    dic[title] = "SPAM"
            else:
                    dic[title] = "OK"
        self.write_to_file(dic, path + "/!prediction.txt")


