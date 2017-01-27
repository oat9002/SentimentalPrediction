import os
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.filters import Filter
from weka.core.classes import Random


### load a dataset CSV ###
def load_dataset(path):
    train_file = path
    loader = Loader("weka.core.converters.CSVLoader")
    train_data = loader.load_file(train_file)
    train_data.class_is_last()
    return train_data

###  Naive Bayes ###
def naivebay_classifier(data):
    classifier = Classifier("weka.classifiers.bayes.NaiveBayes")
    # classifier.build_classifer(data)
    evaluation = Evaluation(data) 
    evaluation.crossvalidate_model(classifier, data, 10, Random(42)) 
    print(evaluation.summary())
    print(evaluation.confusion_matrix)
    return classifier

jvm.start()
train_data = load_dataset("./output/output_5EMO_2.csv")
naivebay_classifier(train_data)
jvm.stop()



