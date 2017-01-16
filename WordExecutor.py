from pythainlp.segment import segment
import re


def word_cleaning(word):
    temp = re.sub(r'[^ก-ูเ-์]', '', word)
    return temp


def create_keyword_thaionly(word_arr):
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


def frequency_occur_in_keyword(word, keyword):
    freq_table = {}
    for w in keyword:
        freq_table[w] = 0
    segmented_word = segment(word)
    for sw in segmented_word:
        for kw in keyword:
            if sw == kw:
                freq_table[kw] = freq_table[kw] + 1
    return freq_table


# library = []
# library.append("ฉันอยากไปที่  นั่นจังเลย")
# library.append("ฉันอยู่ที่นี่มี ความสุขจัง")
# library.append("ฉันอยาก ไปอีก จัง")
# key = create_keyword_thaionly(library)
# print(key)
# print(sorted(frequency_occur_in_keyword(word = library[0], keyword = key).keys()))