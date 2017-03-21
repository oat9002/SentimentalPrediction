# -*- coding: utf-8 -*-
import CSVExecutor
import WordExecutor
import random
import model
from threading import Thread

def check_emo_in_word(keyword_list, emoji_list, word, emo_count):
    _emo_count = check_emoji_in_word(emoji_list, word)
    for item in keyword_list:
       _emo_count += word.count(item)
    emo_count.append(_emo_count)
    if _emo_count == 0:
        return False
    else:
        return True


def check_emoji_in_word(emoji_list, word):
    count = 0
    word = word.split(' ')
    #cleaning word
    for idx, w in enumerate(word):
        if 'http' in w:
            del word[idx]
    word = ' '.join(word)
    #start checking
    for item in emoji_list:
        count += word.count(item)
    return count

def check_emo(data, emo_count):
    emo_list = data[1:]
    count = 0
    predicted_emo_list = []
    for emo in emo_list:
        if emo == '':
            count += 1
        else:
            predicted_emo_list.append(emo)
    if count == 8:
        data[7] = get_emo(7)
    elif count < 7:
        emo = ''
        emo_max = max(emo_count)
        chk_rand = emo_count.count(emo_max)
        if chk_rand == len(predicted_emo_list):
            rand_num = random.randint(0, len(predicted_emo_list) - 1)
            emo = predicted_emo_list[rand_num]
        elif chk_rand == 1:
            for idx, i in enumerate(emo_count):
                if i == emo_max:
                    emo = get_emo(idx + 1)
                    break
        else:
            emo_max_list = []
            for idx, i in enumerate(emo_count):
                if i == emo_max:
                    emo_max_list.append(idx + 1)
            rand_num = random.randint(0, len(emo_max_list) - 1)
            emo = get_emo(emo_max_list[rand_num])
        data[1:] = [''] * 8
        data[revert_emo_to_number(emo)] = emo
    return data

def get_predicted(data): 
    for i in data[1:]: 
        if i != '': 
            return revert_emo_to_number(i) 

def get_emo(number):
    if number == 1:
        return 'joy'
    elif number == 2:
        return 'sadness'
    elif number == 3:
        return 'fear'
    elif number == 4:
        return 'anger'
    elif number == 5:
        return 'disgust'
    elif number == 6:
        return 'surprise'
    elif number == 7:
        return 'anticipation'
    elif number == 8:
        return 'acceptance'
    else:
        print('Enter a wrong number.')

def revert_emo_to_number(emo):
    if emo == 'joy':
        return 1
    elif emo == 'sadness':
        return 2
    elif emo == 'fear':
        return 3
    elif emo == 'anger' or emo == 'angry':
        return 4
    elif emo == 'disgust':
        return 5
    elif emo == 'surprise':
        return 6
    elif emo == 'anticipation':
        return 7
    elif emo == 'acceptance':
        return 8
    else:
        print('Enter a wrong emo.')


def predict_by_multinominal_naive_bayes(classifier_path, attribute_path, data):
    """
    data: Array
    """
    clf = model.read_model_scikitlearn(classifier_path)
    keywords = CSVExecutor.read_csv(attribute_path)[0]

    freq_test = []
    total_thread = divided_thread_len_end(size=len(data), total_thread=4)
    threads = []
    for i in range(0, len(total_thread)):
        if i != 0:
            t = Thread(target=caculate_freq_for_thread, args=(total_thread[i - 1], total_thread[i], data, freq_test, keywords, 1))
        else:
            t = Thread(target=caculate_freq_for_thread, args=(0, total_thread[i], data, freq_test, keywords, 1))
        threads.append(t)
    start_thread(thread_each_lap=4, threads=threads)

    testset = WordExecutor.to_scikitlearn_dataset(data=freq_test, attribute=sorted(keywords))
    predicted = clf.predict(testset)
    return predicted

def divided_thread_len_end(size, total_thread):
    thread_len_end = []
    temp = 0
    t_size = size
    if size >= total_thread:
        for idx in range(0, total_thread):
            divide = int(size / total_thread)
            if idx != total_thread - 1:
                thread_len_end.append(divide + temp)
                t_size -= divide
            else:
                thread_len_end.append(t_size + temp)
            temp += divide
    else:
        thread_len_end.append(size)
    return thread_len_end


def caculate_freq_for_thread(start, end, dataset, freq, attribute, gram):
    for idx in range(start, end):
        freq.append(WordExecutor.frequency_occur_in_keyword(dataset[idx], attribute, gram))

def start_thread(thread_each_lap, threads):
    idx_start = 0
    idx_join = 0
    if thread_each_lap < len(threads):
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
    else:
        threads[0].start()
        threads[0].join()

if __name__ == '__main__':
    print(predict_by_multinominal_naive_bayes('./Dataset/mnnb.pkl', './Dataset/lated_keyword.csv', ['ไปโรงเรียน']))

