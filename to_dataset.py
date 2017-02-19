import CSVExecutor
import WordExecutor
import threading
import gc

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

library = CSVExecutor.read_csv('./Dataset/8EMO_label.csv')
words = []
for li in library:
    words.append(li[0])
unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
bigram = WordExecutor.create_ngram_from_list_bynltk(words, 2)
trigram = WordExecutor.create_ngram_from_list_bynltk(words, 3)

u = unigram
ub = unigram + bigram
ubt = unigram + bigram + trigram

# u = WordExecutor.remove_stop_word(u)
u = WordExecutor.remove_strange_word_and_normalize(u)

ub = WordExecutor.remove_stop_word(ub)
ub = WordExecutor.remove_strange_word_and_normalize(ub)

ubt = WordExecutor.remove_stop_word(ubt)
ubt = WordExecutor.remove_strange_word_and_normalize(ubt)

total_thread = divided_thread_len_end(size=len(library), total_thread=8)
threads = []
freq = []

def caculate_freq_for_thread(start, end, dataset):
    for idx in range(start, end):
        dataset[idx][0] = WordExecutor.frequency_occur_in_keyword(dataset[idx][0], u, 1)
        freq.append(dataset[idx])

for i in range(0, len(total_thread)):
    if i != 0:
        t = threading.Thread(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], library,))
    else:
        t = threading.Thread(target=caculate_freq_for_thread, args=(0, total_thread[i], library,))
    threads.append(t)

threads[0].start()
threads[1].start()
threads[0].join()
threads[1].join()
gc.collect()
threads[2].start()
threads[3].start()
threads[2].join()
threads[3].join()
gc.collect()
threads[4].start()
threads[5].start()
threads[4].join()
threads[5].join()
gc.collect()
threads[6].start()
threads[7].start()
threads[6].join()
threads[7].join()

# freq = []
# for li in library:
#     li[0] = WordExecutor.frequency_occur_in_keyword(li[0], ub, 2)
#     freq.append(li)
# keywords = []
# keywords.append(u)
# print(CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
CSVExecutor.write_csv('output/test_thread.csv', CSVExecutor.to_dataset_format(freq, sorted(freq[0][0].keys())))
# CSVExecutor.write_csv('output/keyword8.csv', keywords)
