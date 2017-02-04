import CSVExecutor
import WordExecutor
import random

def check_emo_in_word(emo_list, word):
    u = WordExecutor.createNgram(word=word, gram=1)
    ub = WordExecutor.createNgram(word=word, gram=2)
    ubt = WordExecutor.createNgram(word=word, gram=3)
    for item in emo_list:
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

def get_emo(number):
    if number == 1:
        return 'joy'
    elif number == 2:
        return 'sadness'
    elif number == 3:
        return 'fear'
    elif number == 4:
        return 'angry'
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
    elif emo == 'angry':
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

keyword_list = CSVExecutor.read_csv_without_first_strange_char("Dataset/EMO_LIST.csv")
for idx in range(0, len(keyword_list)):
    while True:
        if '' in keyword_list[idx]:
            keyword_list[idx].remove('')
        else:
            break
# print(keyword_list)
joy_list = keyword_list[0]
joy_list.remove('joy')
sadness_list = keyword_list[1]
sadness_list.remove('sadness')
fear_list = keyword_list[2]
fear_list.remove("fear")
angry_list = keyword_list[3]
angry_list.remove('angry')
disgust_list = keyword_list[4]
disgust_list.remove('disgust')
surprise_list = keyword_list[5]
surprise_list.remove('surprise')
anticipation_list = keyword_list[6]
anticipation_list.remove('anticipation')
acceptance_list = keyword_list[7]
acceptance_list.remove('acceptance')

words = CSVExecutor.read_csv('Dataset/all.csv')
list = []
for wd in words:
    temp = []
    temp.append(wd[0])
    if check_emo_in_word(joy_list, wd[0]):
        temp.append('joy')
    else:
        temp.append('')
    if check_emo_in_word(sadness_list, wd[0]):
        temp.append('sadness')
    else:
        temp.append('')
    if check_emo_in_word(fear_list, wd[0]):
        temp.append('fear')
    else:
        temp.append('')
    if check_emo_in_word(angry_list, wd[0]):
        temp.append('angry')
    else:
        temp.append('')
    if check_emo_in_word(disgust_list, wd[0]):
        temp.append('disgust')
    else:
        temp.append('')
    if check_emo_in_word(surprise_list, wd[0]):
        temp.append('surprise')
    else:
        temp.append('')
    if check_emo_in_word(anticipation_list, wd[0]):
        temp.append('anticipation')
    else:
        temp.append('')
    if check_emo_in_word(acceptance_list, wd[0]):
        temp.append('acceptance')
    else:
        temp.append('')
    list.append(check_emo(temp))
CSVExecutor.write_csv('output/labeled2.csv', list)
# print(joy_list, sadness_list, fear_list, angry_list, disgust_list, surprise_list, anticipation_list, acceptance_list)
