# -*- coding: utf-8 -*-
import CSVExecutor
import WordExecutor
import random
import model

def check_emo_in_word(keyword_list, emoji_list, word):
    if check_emoji_in_word(emoji_list, word):
        return True
    else:
        u = WordExecutor.createNgram(word=word, gram=1)
        ub = WordExecutor.createNgram(word=word, gram=2)
        ubt = WordExecutor.createNgram(word=word, gram=3)

        for item in keyword_list:
            for w in u:
                if item == w:
                    return True
            for w in ub:
                if item == w:
                    return True
            for w in ubt:
                if item == w:
                    return True
    return False


def check_emoji_in_word(emoji_list, word):
    word = word.split(' ')
    for idx, w in enumerate(word):
        if 'http' in w:
            del word[idx]
    word = ' '.join(word)
    for item in emoji_list:
        if item in word:
            return True
    return False


def check_emo(data):
    emo_list = data[1:]
    count = 0
    predicted_emo_list = []
    for emo in emo_list:
        if emo == '':
            count += 1
        else:
            predicted_emo_list.append(emo)
    if count == 8:
        rand_num = random.randint(1, 8)
        data[rand_num] = get_emo(number=rand_num)
    elif count < 7:
        rand_num = random.randint(0, len(predicted_emo_list) - 1)
        emo = predicted_emo_list[rand_num]
        data[1:] = ['']*8
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


"""
data: Array
"""
def predict_by_multinominal_naive_bayes(classifier_path, keywords_path, data):
    clf = model.read_model_scikitlearn(classifier_path)
    keywords = CSVExecutor.read_csv(keywords_path)[0]

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
        hread_len_end.append(size)
    return thread_len_end


def caculate_freq_for_thread(start, end, dataset, freq, keyword, gram):
    for idx in range(start, end):
        freq.append(WordExecutor.frequency_occur_in_keyword(dataset[idx], keyword, gram))

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

