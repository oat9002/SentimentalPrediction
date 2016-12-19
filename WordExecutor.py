from pythainlp.segment import segment


def create_keyword_thaionly(word_arr):
    keywords = []
    exist = False
    for item in word_arr:
        segmented_word = segment(item)
        for sw in segmented_word:
            for existedWord in keywords:
                if sw == existedWord:
                    exist = True
                    break
            if not exist:
                keywords.append(sw)
            exist = False
    return keywords


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
# library.append("ฉันอยากไปที่นั่นจังเลย")
# library.append("ฉันอยู่ที่นี่มีความสุขจัง")
# library.append("ฉันอยากไปอีกจัง")
# key = create_keyword_thaionly(library)
# print(key)
# print(sorted(frequency_occur_in_keyword(word = library[0], keyword = key).keys()))
