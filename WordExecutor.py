from pythainlp.segment import segment
import re
from nltk.util import ngrams
import CSVExecutor

emoji = CSVExecutor.read_csv('Dataset/EMOJI_LIST.csv')
emoji_list = []
for i in emoji:
    for j in i:
        emoji_list.append(j)

"""
word: any words you want to clean
"""
def word_cleaning(word):
    only_thai = re.sub(r'[^ก-ูเ-์]', '', word)
    only_thai = re.sub(r'ๆ', '', only_thai)
    only_thai = re.sub(r'ๅ', '', only_thai)
    only_thai = re.sub(r'ฯ', '', only_thai)
    except_word = ['กก']
    idx = 0
    while idx < len(only_thai):
        ch_t = only_thai[idx]
        idx_t = idx + 1
        duplicate = False
        while True:
            if idx_t < len(only_thai):
                if ch_t == only_thai[idx_t]:
                    idx_t += 1
                    duplicate = True
                else:
                    break
            else:
                break
        if duplicate:
            omit = False
            for ex in except_word:
                if ex == only_thai[idx: idx_t]:
                    omit = True
                    break
            if not omit:
                if idx_t != len(only_thai) - 1:
                    only_thai = only_thai[:idx + 1] + only_thai[idx_t:]
                else:
                    only_thai = only_thai[:idx + 1]
        idx += 1
    return only_thai

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


def frequency_occur_in_keyword(word, keyword):
    freq_table = {}
    for w in keyword:
        freq_table[w] = 0
    for kw in keyword:
        if kw not in emoji_list:
            freq_table[kw] = word_cleaning(word).count(kw)
        else:
            freq_table[kw] = word.count(kw)
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

def add_emoji_keyword(keyword_list):
    for item in emoji_list:
        keyword_list.append(item)
    return keyword_list

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

# word = "กกกกกใข่"
# print(word_cleaning(word))
# remove_strangeword(123)
# library.append("ฉันอยู่ที่นี่มี ความสุขจัง")
# library.append("ฉันอยาก ไปอีก จัง")
# key = create_keyword_thaionly(library)
# print(key)
# print(sorted(frequency_occur_in_keyword(word = library[0], keyword = key).keys()))
