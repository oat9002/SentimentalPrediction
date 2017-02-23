import numpy as np
from sklearn.naive_bayes import MultinomialNB
import CSVExecutor
import WordExecutor
import model
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.feature_extraction.text import TfidfTransformer

library = CSVExecutor.read_csv('./Dataset/8EMO_label.csv')
words = []
for li in library:
    words.append(li[0])
unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
# bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
# trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

u = unigram
# ub = unigram + bigram
# ubt = unigram + bigram + trigram

# u = WordExecutor.remove_stop_word(u)
u = WordExecutor.remove_strange_word_and_normalize(u)

# ub = WordExecutor.remove_stop_word(ub)
# ub = WordExecutor.remove_strange_word_and_normalize(ub)

# ubt = WordExecutor.remove_stop_word(ubt)
# ubt = WordExecutor.remove_strange_word_and_normalize(ubt)


freq = []
for li in library:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
    freq.append(li)

dataset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
target = WordExecutor.get_labeled_class(data=freq)

tfidf_transformer = TfidfTransformer()
tfidf = tfidf_transformer.fit_transform(dataset)

clf = MultinomialNB()
clf.fit(dataset, target)


# clf = model.read_model_scikitlearn('./output/model.pkl')
# model.save_model_scikitlearn(classifier=clf, path='output/model.pkl')

# test = CSVExecutor.read_csv('./Dataset/ktest.csv')
# freq = []
# for li in test:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
#     freq.append(li)
# testset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
# testtarget = WordExecutor.get_labeled_class(data=freq)
# predicted = cross_val_predict(clf, dataset, target, cv=10)

test = CSVExecutor.read_csv('./Dataset/test_NSC.csv')

freq_test = []
for li in test:
    li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
    freq_test.append(li)

testset = WordExecutor.to_scikitlearn_dataset(data=freq_test, attribute=sorted(u))
test_target = WordExecutor.get_labeled_class(data=freq_test)

predicted = clf.predict(testset)

np.mean(predicted == test_target)  
# print(metrics.accuracy_score(test_target, predicted))
# print(metrics.classification_report(test_target, predicted))
# print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
