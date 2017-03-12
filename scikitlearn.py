import numpy as np
from sklearn.naive_bayes import MultinomialNB
import CSVExecutor
import WordExecutor
import model
from sklearn import metrics
from sklearn.model_selection import cross_val_predict
from sklearn.feature_extraction.text import TfidfTransformer
from threading import Thread
from time import time

def divided_thread_len_end(size, total_thread):
    thread_len_end = []
    temp = 0
    t_size = size
    for idx in range(0, total_thread):
        divide = int(size / total_thread)
        if idx != total_thread - 1:
            thread_len_end.append(divide + temp)
            t_size -= divide
        else:
            thread_len_end.append(t_size + temp)
        temp += divide
    return thread_len_end


def caculate_freq_for_thread(start, end, dataset, freq, keyword, gram):
    for idx in range(start, end):
        dataset[idx][0] = WordExecutor.frequency_occur_in_keyword(dataset[idx][0], keyword, gram)
        freq.append(dataset[idx])

def start_thread(thread_each_lap, threads):
    idx_start = 0
    idx_join = 0
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


if __name__ == '__main__':
    now = time()
    library = CSVExecutor.read_csv('./output/For paper/train_1+2_formatted.csv')
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

    # freq = []
    # total_thread = divided_thread_len_end(size=len(library), total_thread=4)
    # threads = []
    # for i in range(0, len(total_thread)):
    #     if i != 0:
    #         t = Thread(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], library, freq, u, 1))
    #     else:
    #         t = Thread(target=caculate_freq_for_thread, args=(0, total_thread[i], library, freq, u, 1))
    #     threads.append(t)
    # start_thread(thread_each_lap=4, threads=threads)

    # dataset = WordExecutor.to_scikitlearn_dataset(data=freq, attribute=sorted(u))
    # target = WordExecutor.get_labeled_class(data=freq)

    # # tfidf_transformer = TfidfTransformer()
    # # tfidf = tfidf_transformer.fit_transform(dataset)

    # clf = MultinomialNB()
    # clf.fit(dataset, target)


    clf = model.read_model_scikitlearn('./output/mnnb.pkl')
    # model.save_model_scikitlearn(classifier=clf, path='output/mnnb.pkl')

    test = CSVExecutor.read_csv('./output/For paper/train_2_formatted.csv')
    
    freq_test = []
    total_thread = divided_thread_len_end(size=len(test), total_thread=4)
    threads = []
    for i in range(0, len(total_thread)):
        if i != 0:
            t = Thread(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], test, freq_test, u, 1))
        else:
            t = Thread(target=caculate_freq_for_thread, args=(0, total_thread[i], test, freq_test, u, 1))
        threads.append(t)
    start_thread(thread_each_lap=4, threads=threads)

    print('Here')
    testset = WordExecutor.to_scikitlearn_dataset(data=freq_test, attribute=sorted(u))
    test_target = WordExecutor.get_labeled_class(data=freq_test)

    predicted = clf.predict(testset)
    print(predicted)

    np.mean(predicted == test_target)
    print(metrics.accuracy_score(test_target, predicted))
    print(time() - now)
    # print(metrics.classification_report(test_target, predicted))
    # print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
