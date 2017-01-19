import CSVExecutor
import WordExecutor

library = CSVExecutor.read_csv('test.csv')
words = []
for li in library:
    words.append(li[0]) # print(words)
unigram = WordExecutor.create_keyword_unigram(words)
bigram = WordExecutor.create_keyword_bigram(words)
trigram = WordExecutor.create_keyword_trigram(words)
print(len(unigram))
print(len(bigram))
print(len(trigram))


# mergedArr = unigram + bigram + trigram
# print(mergedArr)
# freq = []
# for li in library:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], mergedArr, 3)
#     freq.append(li)
# print(freq)
# # print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
# CSVExecutor.write_csv('test2.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))