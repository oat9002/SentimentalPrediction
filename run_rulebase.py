import rulebase
import CSVExecutor

keyword_list = CSVExecutor.read_csv_without_first_strange_char("Dataset/KEYWORD_LIST.csv")
emoji_list = CSVExecutor.read_csv("Dataset/EMOJI_LIST.csv")
icon_list = CSVExecutor.read_csv("Dataset/ICON_LIST.csv")


for idx in range(0, len(keyword_list)):
    while True:
        if '' in keyword_list[idx]:
            keyword_list[idx].remove('')
        else:
            break

joy_list = keyword_list[0]
sadness_list = keyword_list[1]
fear_list = keyword_list[2]
anger_list = keyword_list[3]
disgust_list = keyword_list[4]
surprise_list = keyword_list[5]
anticipation_list = keyword_list[6]
acceptance_list = keyword_list[7]
# acceptance_list.remove('acceptance')


joy_list_emo = emoji_list[0]+icon_list[0]
sadness_list_emo = emoji_list[1]+icon_list[1]
fear_list_emo = emoji_list[2]+icon_list[2]
anger_list_emo = emoji_list[3]+icon_list[3]
disgust_list_emo = emoji_list[4]+icon_list[4]
surprise_list_emo = emoji_list[5]+icon_list[5]
anticipation_list_emo = emoji_list[6]+icon_list[6]
acceptance_list_emo = emoji_list[7]+icon_list[7]

# print(joy_list_emo)
# print(sadness_list_emo)
# print(fear_list_emo)
# print(anger_list_emo)
# print(disgust_list_emo)
# print(surprise_list_emo)
# print(anticipation_list_emo)
# print(acceptance_list_emo)

words = CSVExecutor.read_csv('Dataset/Ktest/test_emoji.csv')
list = []
for wd in words:
    temp = []
    emo_count = []
    temp.append(wd[0])
    if rulebase.check_emo_in_word(joy_list,joy_list_emo, wd[0], emo_count):
        temp.append('joy')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(sadness_list,sadness_list_emo, wd[0], emo_count):
        temp.append('sadness')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(fear_list,fear_list_emo, wd[0], emo_count):
        temp.append('fear')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(anger_list,anger_list_emo, wd[0], emo_count):
        temp.append('anger')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(disgust_list,disgust_list_emo, wd[0], emo_count):
        temp.append('disgust')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(surprise_list,surprise_list_emo, wd[0], emo_count):
        temp.append('surprise')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(anticipation_list,anticipation_list_emo, wd[0], emo_count):
        temp.append('anticipation')
    else:
        temp.append('')
    if rulebase.check_emo_in_word(acceptance_list,acceptance_list_emo, wd[0], emo_count):
        temp.append('acceptance')
    else:
        temp.append('')
    list.append(rulebase.check_emo(temp, emo_count))
CSVExecutor.write_csv('output/labeled_test_emoji.csv', list)
# print(joy_list, sadness_list, fear_list, angry_list, disgust_list, surprise_list, anticipation_list, acceptance_list)
