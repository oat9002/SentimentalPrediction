import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import CSVExecutor
import WordExecutor
from sklearn.feature_extraction import DictVectorizer


library = CSVExecutor.read_csv('./Dataset/4EMO.csv')
words = []
for li in library:
    words.append(li[0])
unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

u = unigram
ub = unigram + bigram
ubt = unigram + bigram + trigram

# u = WordExecutor.remove_stop_word(u)
u = WordExecutor.remove_strange_word_and_normalize(u)

ub = WordExecutor.remove_stop_word(ub)
ub = WordExecutor.remove_strange_word_and_normalize(ub)

ubt = WordExecutor.remove_stop_word(ubt)
ubt = WordExecutor.remove_strange_word_and_normalize(ubt)


freq = []
for li in library:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
    freq.append(li)

dataset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
target = WordExecutor.get_labeled_class(data=freq)
clf = MultinomialNB()
clf.fit(dataset, target)

test = CSVExecutor.read_csv('./Dataset/ktest.csv')
freq = []
for li in test:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
    freq.append(li)
testset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
testtarget = WordExecutor.get_labeled_class(data=freq)
predicted = clf.predict(testset)
print(np.mean(predicted == testtarget))
