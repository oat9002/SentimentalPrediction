import CSVExecutor
import WordExecutor


library = CSVExecutor.read_csv('./Dataset/5EMO.csv')
words = []
for li in library:
    words.append(li[0])

unigram = WordExecutor.create_ngram_bynltk(words, 1)
bigram = WordExecutor.create_ngram_bynltk(words, 2)
trigram = WordExecutor.create_ngram_bynltk(words, 3)

mergedArr = unigram + bigram + trigram
print(mergedArr)
freq = []
for li in library:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], mergedArr, 3)
    freq.append(li)
# print(freq)
# print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
CSVExecutor.write_csv('test3.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))