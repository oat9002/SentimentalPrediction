from pythainlp.segment import segment
import re

"""
word: any words you want to clean
"""
def word_cleaning(word):
    temp = re.sub(r'[^ก-ูเ-์]', '', word)
    return temp

"""
word_arr: list of words from file.
"""
def create_keyword_unigram(word_arr):
    keywords = []
    exist = False
    for item in word_arr:
        segmented_word = segment(word_cleaning(item))
        for sw in segmented_word:
            for existedWord in keywords:
                if sw == existedWord:
                    exist = True
                    break
            if not exist:
                keywords.append(sw)
            exist = False
    return keywords


"""
word_arr: list of words from file.
"""
def create_keyword_bigram(word_arr):
    bigram = []
    exist = False
    for item in word_arr:
        segmented_word = segment(word_cleaning(item))
        for idx in range(0, len(segmented_word)):
            if idx < (len(segmented_word) - 1):
                bi_str = segmented_word[idx] + segmented_word[idx + 1]
                for existedWord in bigram:
                    if bi_str == existedWord:
                        exist = True
                        break
                if not exist:
                    bigram.append(bi_str)
    return bigram

"""
word_arr: list of words from file.
"""
def create_keyword_trigram(word_arr):
    trigram = []
    exist = False
    for item in word_arr:
        segmented_word = segment(word_cleaning(item))
        for idx in range(0, len(segmented_word)):
            if idx < (len(segmented_word) - 2):
                bi_str = segmented_word[idx] + segmented_word[idx + 1] + segmented_word[idx + 2]
                for existedWord in trigram:
                    if bi_str == existedWord:
                        exist = True
                        break
                if not exist:
                    trigram.append(bi_str)
    return trigram


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
    for sw in segmented_word:
        for kw in keyword:
            if sw == kw:
                freq_table[kw] = freq_table[kw] + 1
    return freq_table

"""
word: word you want to create N-gram
type:   1 - unigram
        2 - bigram
        3 - trigram
"""


def createNgram(word, type):
    segmented_word = segment(word_cleaning(word))
    ret_word = []
    for idx in range(0, len(segmented_word)):
        w_str = ""
        if idx < (len(segmented_word) - (type - 1)):
            for i in range(0, type):
                if i == 0:
                    w_str = segmented_word[idx + i]
                else:
                    w_str = w_str + segmented_word[idx + i]
            ret_word.append(w_str)
    return ret_word


# library = []
# library.append("ฉันอยากไปที่  นั่นจังเลย")
# library.append("ฉันอยู่ที่นี่มี ความสุขจัง")
# library.append("ฉันอยาก ไปอีก จัง")
# key = create_keyword_thaionly(library)
# print(key)
# print(sorted(frequency_occur_in_keyword(word = library[0], keyword = key).keys()))