from collections import Counter

def read_classification_from_file(fname):
    classification = {}
    with open(fname, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.split()

            classification[words[0]] = words[1]
    return classification

def word_freq_in_file(arg):
    counter = Counter()
    array = arg.split('\n\n', 1)[1]
    array = array.split()
    count = 0
    for word in array:
        temp_word = word.lower()
        counter[temp_word] += 1
        count += 1
    return counter, count

