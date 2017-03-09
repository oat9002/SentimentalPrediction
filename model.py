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
import rulebase

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
def multinominal_naive_bayes_classifier(dataset, target):
    clf = MultinomialNB()
    clf.fit(dataset, target)
    return clf

def predict_for_result(classifier, test_set):
    return classifier.predict(test_set)

def save_model_scikitlearn(classifier, path):
    joblib.dump(classifier, path)

def read_model_scikitlearn(path):
    return joblib.load(path)
