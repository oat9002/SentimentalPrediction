import CSVExecutor
import WordExecutor
import random
import emoji


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
