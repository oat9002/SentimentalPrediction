from pythainlp.segment import segment
import re
from nltk.util import ngrams
import CSVExecutor
from threading import Thread

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
    except_char = ['ั', 'ี', 'ึ', 'ิ', 'ื']
    except_word = ['กก', 'เเ']
    idx = 0
    while idx < len(only_thai):
        ch_t = only_thai[idx]
        idx_t = idx + 1
        duplicate = False
        while True:
            if idx_t < len(only_thai):
                if ch_t == only_thai[idx_t]:
                    idx_t += 1
                    if idx_t < len(only_thai) and only_thai[idx_t] not in except_char:
                        duplicate = True
                    else:
                        break
                else:
                    break
            else:
                break
        if duplicate:
            omit = False
            if only_thai[idx: idx_t] in except_word:
                omit = True
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


def frequency_occur_in_keyword(word, keyword, maxGram):
    freq_table = {}
    segmented_word = []
    for w in keyword:
        freq_table[w] = 0
    for t in range(1, maxGram + 1): 
        segmented_word = segmented_word + createNgram(word, t) 
    for kw in keyword:
        if kw not in emoji_list:
            freq_table[kw] = segmented_word.count(kw)
        else:
            freq_table[kw] = word.count(kw)
    del segmented_word
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

def _to_scikitlearn_dataset(start, end, data, attribute, formatted):
    for i in range(start, end):
        freq_t = []
        for h in attribute:
            if h != 'class':
                if len(data[i] > 1):
                    freq_t.append(data[i][0].get(h))
                else:
                    freq_t.append(data[i].get(h))
        formatted[i] = freq_t

def to_scikitlearn_dataset(data, attribute):
    threads = []
    formatted = [None] * len(data)
    divided = divided_thread_len_end(len(data), total_thread=4)
    for i in range(0, len(divided)):
        if i != 0:
            t = Thread(target=_to_scikitlearn_dataset, args=(divided[i - 1], divided[i], data, attribute, formatted))
        else:
            t = Thread(target=_to_scikitlearn_dataset, args=(0, divided[i], data, attribute, formatted))
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return formatted

def get_labeled_class(data):
    classes = []
    for item in data:
        classes.append(item[1])
    return classes

def divided_thread_len_end(size, total_thread):
    thread_len_end = []
    temp = 0
    t_size = size
    if(size >= total_thread):
        for idx in range(0, total_thread):
            divide = int(size / total_thread)
            if idx != total_thread - 1:
                thread_len_end.append(divide + temp)
                t_size -= divide
            else:
                thread_len_end.append(t_size + temp)
            temp += divide
    else:
        thread_len_end.append(size)
    return thread_len_end

if __name__ == '__main__':
    a = "มากกกกกกโขขขขขขวันนี้้้้้้้้มาแว้ววว"
    print(word_cleaning(a))

