import os
from weka.core.converters import Loader
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.filters import Filter
from weka.core.classes import Random
import weka.core.serialization as serialization
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.model_selection import cross_val_predict
from sklearn.feature_extraction.text import TfidfTransformer
import rulebase
import WordExecutor
import CSVExecutor
from threading import Thread

############################# Weka ###################################################
"""
Load dataset

path: path where you want to load dataset
"""
def load_dataset_weka(path):
    train_file = path
    loader = Loader("weka.core.converters.CSVLoader")
    train_data = loader.load_file(train_file)
    train_data.class_is_last()
    return train_data

"""
Create classifier by naive bayes algrorithm

data: data you want to train
"""
def naivebay_classifier_weka(data):
    classifier = Classifier("weka.classifiers.bayes.NaiveBayes")
    evaluation = Evaluation(data)
    evaluation.crossvalidate_model(classifier, data, 10, Random(42))
    print(evaluation.summary())
    print(evaluation.confusion_matrix)
    return classifier


"""
Classify

data: data you want to classify
classifier: your model
"""
def predict_for_result_weka(classifier, data):
    classifier.build_classifier(data)
    return Classifier.classify_instance(data)


"""
Write a model to disk

classifier: model that you want to write
path: path where you want to write
"""
def save_model_weka(classifier, path):
    serialization.write(path, classifier)


"""
Read a model from disk

path: path where you want to read
"""
def read_model_weka(path):
    return Classifier(jobject=serialization.read(path))

"""
Fill empty data in column 10 if column 9 is 1
"""
def reformatted_data(data):
    stm = data[1:9]
    if data[9] != 1:
        for i in stm:
            if i != '':
                emo = rulebase.revert_emo_to_number(i)
                data[10] = emo
    del data[1:10]
    return data



######################### Scikit Learn #########################################
def multinominal_naive_bayes_classifier_with_tfidf(dataset_path):
    library = CSVExecutor.read_csv(dataset_path)
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
    total_thread = divided_thread_len_end(size=len(library), total_thread=8)
    threads = []
    for i in range(0, len(total_thread)):
        if i != 0:
            t = Thread(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], library, freq, u, 1))
        else:
            t = Thread(target=caculate_freq_for_thread, args=(0, total_thread[i], library, freq, u, 1))
        threads.append(t)
    start_thread(thread_each_lap=4, threads=threads)

    dataset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
    target = WordExecutor.get_labeled_class(data=freq)

    tfidf_transformer = TfidfTransformer()
    tfidf = tfidf_transformer.fit_transform(dataset)
    clf = MultinomialNB()
    clf.fit(tfidf, target)
    return clf

def multinominal_naive_bayes_classifier(dataset_path):
    library = CSVExecutor.read_csv(dataset_path)
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
    total_thread = divided_thread_len_end(size=len(library), total_thread=8)
    threads = []
    for i in range(0, len(total_thread)):
        if i != 0:
            t = Thread(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], library, freq, u, 1))
        else:
            t = Thread(target=caculate_freq_for_thread, args=(0, total_thread[i], library, freq, u, 1))
        threads.append(t)
    start_thread(thread_each_lap=4, threads=threads)

    dataset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
    target = WordExecutor.get_labeled_class(data=freq)

    clf = MultinomialNB()
    clf.fit(dataset, target)
    return clf

def predict_for_result(classifier, test_set):
    return classifier.predict(test_set)

def save_model_scikitlearn(classifier, path):
    joblib.dump(classifier, path)

def read_model_scikitlearn(path):
    return joblib.load(path)

def divided_thread_len_end(size, total_thread):
    thread_len_end = []
    temp = 0
    t_size = size
    if size >= total_thread:
        for idx in range(0, total_thread):
            divide = int(size / total_thread)
            if idx != total_thread - 1:
                thread_len_end.append(divide + temp)
                t_size -= divide
            else:
                thread_len_end.append(t_size + temp)
            temp += divide
    else:
        thread_len_end.append(size)
    return thread_len_end

def caculate_freq_for_thread(start, end, dataset, freq, keyword, gram):
    for idx in range(start, end):
        freq.append(WordExecutor.frequency_occur_in_keyword(dataset[idx], keyword, gram))

def start_thread(thread_each_lap, threads):
    idx_start = 0
    idx_join = 0
    if thread_each_lap < len(threads):
        while idx_start < len(threads) or idx_join < len(threads):
            for i in range(0, thread_each_lap):
                if idx_start < len(threads):
                    threads[idx_start].start()
                    idx_start += 1
                else:
                    break
            for i in range(0, thread_each_lap):
                if idx_join < len(threads):
                    threads[idx_join].join()
                    # print('Finish thread: ' + str(idx_join + 1))
                    idx_join += 1 
                else:
                    break
    else:
        threads[0].start()
        threads[0].join()