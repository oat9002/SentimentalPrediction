import os
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.filters import Filter
from weka.core.classes import Random
import weka.core.serialization as serialization


"""
Load dataset

path: path where you want to load dataset
"""
def load_dataset(path):
    train_file = path
    loader = Loader("weka.core.converters.CSVLoader")
    train_data = loader.load_file(train_file)
    train_data.class_is_last()
    return train_data

"""
Classify with naive bayes algrorithm

data: data you want to train
"""
def naivebay_classifier(data):
    classifier = Classifier("weka.classifiers.bayes.NaiveBayes")
    # classifier.build_classifer(data)
    evaluation = Evaluation(data) 
    evaluation.crossvalidate_model(classifier, data, 10, Random(42)) 
    print(evaluation.summary())
    print(evaluation.confusion_matrix)
    return classifier


"""
Write a model to disk

classifier: model that you want to write
path: path where you want to write
"""
def save_model(classifier, path):
    serialization.write(path, classifier)


"""
Read a model from disk

path: path where you want to read
"""
def read_model(path):
    return Classifier(jobject=serialization.read(path))

jvm.start()
train_data = load_dataset("./output/output_5EMO_2.csv")
naivebay_classifier(train_data)
jvm.stop()



