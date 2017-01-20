import CSVExecutor
import WordExecutor


library = CSVExecutor.read_csv('./Dataset/5EMO.csv')
words = []
for li in library:
    words.append(li[0])

unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

a = unigram
b = unigram + bigram
mergedArr = unigram + bigram + trigram

print(len(a))
print(len(b))
print(len(mergedArr))

a = WordExecutor.remove_stopword(a)
# a = WordExecutor.remove_strangeword(a)

b = WordExecutor.remove_stopword(b)
# b = WordExecutor.remove_strangeword(b)

mergedArr = WordExecutor.remove_stopword(mergedArr)
# mergedArr = WordExecutor.remove_strangeword(mergedArr)

print("after that")
print(len(set(a)))
print(len(set(b)))
print(len(set(mergedArr)))

# print(mergedArr)
# freq = []
# for li in library:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], mergedArr, 3)
#     freq.append(li)

# print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
# CSVExecutor.write_csv('test4.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))