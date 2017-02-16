import CSVExecutor
import WordExecutor


library = CSVExecutor.read_csv('./Dataset/8EMO.csv')
words = []
for li in library:
    words.append(li[0])
unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

u = unigram
ub = unigram + bigram
ubt = unigram + bigram + trigram

u = WordExecutor.remove_stop_word(u)
u = WordExecutor.remove_strange_word_and_normalize(u)

ub = WordExecutor.remove_stop_word(ub)
ub = WordExecutor.remove_strange_word_and_normalize(ub)

ubt = WordExecutor.remove_stop_word(ubt)
ubt = WordExecutor.remove_strange_word_and_normalize(ubt)

# print(ubt)
freq = []
for li in library:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
    freq.append(li)

# keywords = []
# keywords.append(u)
# print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
CSVExecutor.write_csv('output/output_8EMO_2.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
# CSVExecutor.write_csv('output/keyword8.csv', keywords)
