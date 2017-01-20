import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import CSVExecutor
import WordExecutor
from pandas import DataFrame

library = CSVExecutor.read_csv('./Dataset/ktest.csv')
words = []
for li in library:
    words.append(li[0])
unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

a = unigram
b = unigram + bigram
mergedArr = unigram + bigram + trigram

# freq = []
# for li in library:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], mergedArr, 3)
#     freq.append(li)
with open("./Dataset/stop_word.txt", "r" , encoding='utf-8') as file:
    stop_words = file.readline()
    stop_words = stop_words.split(' ')
    stop_words[0] = stop_words[0][1:]

    count_vectorizer = CountVectorizer(ngram_range=(1,1), stop_words=stop_words)
    print(count_vectorizer.build_analyzer()("ฉันอยากไปโรงเรียนจุง"))
    # counts = count_vectorizer.fit_transform(words)
    # print(counts.get

# X = np.random.randint(5, size=(6, 100))
# y = np.array([1, 2, 3, 4, 5, 6])

# clf = MultinomialNB()
# clf.fit(X, y)

# print(clf.predict(X[2:3]))