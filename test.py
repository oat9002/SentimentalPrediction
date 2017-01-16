import CSVExecutor
import WordExecutor

library = CSVExecutor.read_csv('test.csv')
words = []
for li in library:
    words.append(li[0])
# print(words)
keywords = WordExecutor.create_keyword_thaionly(words)
bigram = WordExecutor.create_keyword_bigram(words)
trigram = WordExecutor.create_keyword_trigram(words)
print(keywords)
print(bigram)
print(trigram)


# freq = []
# for li in library:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], keywords)
#     freq.append(li)
# print(freq)
# print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
# CSVExecutor.write_csv('test2.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))