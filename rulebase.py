import CSVExecutor
import WordExecutor

def check_emo_in_word(emo_list, word):
    for item in emo_list:
        if item in wd[0]:
            return True
    return False

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
        temp.append('disgust_list')
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
    list.append(temp)
CSVExecutor.write_csv('output/labeled.csv', list)
# print(joy_list, sadness_list, fear_list, angry_list, disgust_list, surprise_list, anticipation_list, acceptance_list)
