import model
import CSVExecutor
import WordExecutor
import weka.core.jvm as jvm
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.core.classes import Random
#
# keywords = CSVExecutor.read_csv('output/keyword.csv')
#
# library = CSVExecutor.read_csv('./Dataset/ktest.csv')
# freq = []
# for li in library:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], keywords[0], 1)
#     freq.append(li[0])
#
# jvm.start()
# train_data = model.load_dataset_weka("./output/output_8EMO.csv")
# clsf = model.naivebay_classifier(train_data)
# model.save_model(clsf, 'output/out8.model')
# # clsf = model.read_model('output/out.model')
# result = model.predict_for_result(clsf, freq[0])
# print(str(result))
# jvm.stop()

jvm.start()
### load a dataset ###
train_data = model.load_dataset_weka("./output/output_8EMO_U.csv") #

###  Naive Bayes ### Choose what you want
classifier = Classifier("weka.classifiers.bayes.NaiveBayesMultinomial")
# classifier = Classifier("weka.classifiers.bayes.NaiveBayes")
# classifier.build_classifer(train_data)
evaluation = Evaluation(train_data)
evaluation.crossvalidate_model(classifier, train_data, 10, Random(42))
print(evaluation.summary())
print(evaluation.confusion_matrix)


    # ###  Naive Bayes ###
    # mlp = Classifier("weka.classifiers.bayes.Naive Bayes")
    # mlp.build_classifer(train_file_5EMO)

jvm.stop()
