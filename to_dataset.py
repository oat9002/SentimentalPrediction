import CSVExecutor
import WordExecutor
import threading
from multiprocessing import Process, Manager
import gc
import time

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
        freq.append(dataset[idx][0])

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
                print('Finish thread: ' + str(idx_join + 1))
                idx_join += 1 
            else:
                break

if __name__ == '__main__':   
    now = time.time() 
    freq = Manager().list()
    library = CSVExecutor.read_csv('./Dataset/8EMO_label.csv')
    words = []
    for li in library:
        words.append(li[0])
    unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
    bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
    trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

    u = WordExecutor.add_emoji_keyword(unigram)
    ub = WordExecutor.add_emoji_keyword(unigram + bigram)
    ubt = WordExecutor.add_emoji_keyword(unigram + bigram + trigram)

    # u = WordExecutor.remove_stop_word(u)
    u = WordExecutor.remove_strange_word_and_normalize(u)

    ub = WordExecutor.remove_stop_word(ub)
    ub = WordExecutor.remove_strange_word_and_normalize(ub)

    ubt = WordExecutor.remove_stop_word(ubt)
    ubt = WordExecutor.remove_strange_word_and_normalize(ubt)

    total_thread = divided_thread_len_end(size=len(library), total_thread=4)
    threads = []
    for i in range(0, len(total_thread)):
        if i != 0:
            t = Process(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], library, freq, u, 1))
        else:
            t = Process(target=caculate_freq_for_thread, args=(0, total_thread[i], library, freq, u, 1))
        threads.append(t)
    print('Here')
    start_thread(thread_each_lap=4, threads=threads)
    print(len(freq))
    # CSVExecutor.write_csv('output/test_process.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
    print(time.time() - now)

    # freq = []
    # for li in library:
    #     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], u, 1)
    #     freq.append(li)
    # keywords = []
    # keywords.append(u)
    # print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
    # CSVExecutor.write_csv('output/test_thread.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
    # CSVExecutor.write_csv('output/keyword8.csv', keywords)
