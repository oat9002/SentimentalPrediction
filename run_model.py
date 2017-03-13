import model
import CSVExecutor
import WordExecutor
import weka.core.jvm as jvm
from weka.classifiers import Evaluation
from weka.classifiers import Classifier
from weka.core.classes import Random
from weka.filters import Filter
import time
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
def run(dataset_path):
    start = time.time()
    
    ### load a dataset ###
    train_data = model.load_dataset_weka(dataset_path) #
    to_nomial_class_filter = Filter(classname="weka.filters.unsupervised.attribute.NumericToNominal", options=["-R", "last"])
    to_nomial_class_filter.inputformat(train_data)
    
    ###  Naive Bayes ### Choose what you want
    classifier = Classifier("weka.classifiers.bayes.NaiveBayesMultinomial")
    # classifier = Classifier("weka.classifiers.bayes.NaiveBayes")
    # classifier.build_classifer(train_data)
    evaluation = Evaluation(to_nomial_class_filter.filter(train_data))
    evaluation.crossvalidate_model(classifier, to_nomial_class_filter.filter(train_data), 10, Random(42))
    # print(evaluation.summary())
    # print(evaluation.class_details())
    # print(evaluation.matrix())
    


        # ###  Naive Bayes ###
        # mlp = Classifier("weka.classifiers.bayes.Naive Bayes")
        # mlp.build_classifer(train_file_5EMO)

    print(time.time() - start)

if __name__ == '__main__':
    jvm.start(max_heap_size="5g")
    print('train_1_with_emoticon')
    for i in range(0,10):
        run('./output/For paper/train_1_with_emoticon.csv')
    # print('\ntrain_1+2_with_emoticon')
    # for i in range(0,10):
    #     run('./output/For paper/train_1+2_with_emoticon.csv')
    # print('\ntrain_2_with_emoticon')
    # for i in range(0,10):
    #     run('./output/For paper/train_2_with_emoticon.csv')
    # print('\ntrain_1_without_emoticon')
    # for i in range(0,10):
    #     run('./output/For paper/train_1_without_emoticon.csv')
    # print('\ntrain_1+2_without_emoticon')
    # for i in range(0,10):
    #     run('./output/For paper/train_1+2_without_emoticon.csv')
    # print('\ntrain_2_without_emoticon')
    # for i in range(0,10):
    #     run('./output/For paper/train_2_without_emoticon.csv')
    jvm.stop()