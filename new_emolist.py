import CSVExecutor
import WordExecutor

path = './Dataset/8EMO_label.csv'

joy = CSVExecutor.read_csv_emo(path,'joy')
sadness = CSVExecutor.read_csv_emo(path,'sadness')
fear = CSVExecutor.read_csv_emo(path,'fear')
angry = CSVExecutor.read_csv_emo(path,'angry')
disgust = CSVExecutor.read_csv_emo(path,'disgust')
surprise = CSVExecutor.read_csv_emo(path,'surprise')
anticipation = CSVExecutor.read_csv_emo(path,'anticipation')
acceptance = CSVExecutor.read_csv_emo(path,'acceptance')

emo = acceptance
words_1 = []
for li in emo:
    words_1.append(li[0])

unigram = WordExecutor.create_ngram_from_list_bynltk(words_1, 1)
bigram = WordExecutor.create_ngram_from_list_bynltk(words_1, 2)
trigram = WordExecutor.create_ngram_from_list_bynltk(words_1, 3)

ubt = unigram + bigram + trigram
# ubt = WordExecutor.remove_stop_word(ubt)
# ubt = WordExecutor.remove_strange_word_and_normalize(ubt)

keywords = []
keywords.append(sorted(ubt))
print(sorted(keywords))

CSVExecutor.write_csv('output/acceptance_keyword_ubt.csv', keywords)

