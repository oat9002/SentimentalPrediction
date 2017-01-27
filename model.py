import os
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.filters import Filter
from weka.core.classes import Random

jvm.start()

### load a dataset ###
train_file = "./output/output_5EMO_2.csv"
loader = Loader("weka.core.converters.CSVLoader")
train_data = loader.load_file(train_file)
train_data.class_is_last()

###  Naive Bayes ###
classifier = Classifier("weka.classifiers.bayes.NaiveBayes")
# classifier.build_classifer(train_data)
evaluation = Evaluation(train_data) 
evaluation.crossvalidate_model(classifier, train_data, 10, Random(42)) 
print(evaluation.summary())
print(evaluation.confusion_matrix)

jvm.stop()



