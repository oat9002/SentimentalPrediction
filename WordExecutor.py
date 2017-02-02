from pythainlp.segment import segment
import re
from nltk.util import ngrams


"""
word: any words you want to clean
"""
def word_cleaning(word):
    temp = re.sub(r'[^ก-ูเ-์]', '', word)
    return temp

"""
word_array: list of words
gram : N-gram you want
"""

def create_ngram_from_list_bynltk(word_arr, gram):
    keywords = []
    for item in word_arr:
        segmented_word = segment(word_cleaning(item))
        grams = ngrams(segmented_word, gram)
        for t in grams:
            keywords.append(''.join(t))
    return list(set(keywords))

"""
word:       sentence you want to count frequency
keyword:    array of keyword
maxGram:    max gram
"""


def frequency_occur_in_keyword(word, keyword, maxGram):
    freq_table = {}
    segmented_word = []
    for w in keyword:
        freq_table[w] = 0
    for t in range(1, maxGram + 1):
        if t == 0:
            segmented_word = createNgram(word, t)
        else:
            segmented_word = segmented_word + createNgram(word, t)
    for kw in keyword:
        freq_table[kw] = segmented_word.count(kw)
    return freq_table

"""
word: word you want to create N-gram
type:   1 - unigram
        2 - bigram
        3 - trigram
"""


def createNgram(word, gram):
    segmented_word = segment(word_cleaning(word))
    ret_word = []
    grams = ngrams(segmented_word, gram)
    for t in grams:
        ret_word.append(''.join(t))
    return ret_word

def remove_stop_word(keywords):
    with open("./Dataset/stop_word.txt", "r" , encoding='utf-8') as file:
        stop_words = file.readline()
        stop_words = stop_words.split(' ')
        stop_words[0] = stop_words[0][1:]
        for k in keywords:
            if k in stop_words:
                keywords.remove(k)
        return keywords

def remove_strange_word_and_normalize(keywords):
    if '' in keywords:
        keywords.remove('')
    return list(set(keywords))

def to_scikitlearn_dataset(data, attribute):
    formatted = []
    for item in data:
        freq_t = []
        for h in attribute:
            if h != 'class':
                freq_t.append(item[0].get(h))
        formatted.append(freq_t)
    return formatted

def get_labeled_class(data):
    attrs = []
    for item in data:
        attrs.append(item[1])
    return sorted(attrs)

# remove_strangeword(123)
# library.append("ฉันอยู่ที่นี่มี ความสุขจัง")
# library.append("ฉันอยาก ไปอีก จัง")
# key = create_keyword_thaionly(library)
# print(key)
# print(sorted(frequency_occur_in_keyword(word = library[0], keyword = key).keys()))
