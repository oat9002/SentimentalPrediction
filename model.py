import os
import weka.core.jvm as jvm
from weka.core.dataset import Instances,Instance
from weka.core.converters import Loader
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.filters import Filter


def main():
    ### load a dataset ###
    train_file_5EMO = "C:/Users/kingk/output_new5EMO_1.csv/"
    loader = Loader("weka.core.converters.CSVLoader")
    train5EMO_data = loader.load_file(train_file_5EMO)
    train5EMO_data.class_is_last()



    # ###  Naive Bayes ###
    # mlp = Classifier("weka.classifiers.bayes.Naive Bayes")
    # mlp.build_classifer(train_file_5EMO)




