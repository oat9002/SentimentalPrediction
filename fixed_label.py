import CSVExecutor
import rulebase

keyword_list = CSVExecutor.read_csv_without_first_strange_char("Dataset/KEYWORD_LIST.csv")
emoji_list = CSVExecutor.read_csv("Dataset/EMOJI_LIST.csv")
icon_list = CSVExecutor.read_csv("Dataset/ICON_LIST.csv")
for idx in range(0, len(keyword_list)):
    while True:
        if '' in keyword_list[idx]:
            keyword_list[idx].remove('')
        else:
            break
# print(keyword_list)
joy_list = keyword_list[0]
sadness_list = keyword_list[1]
fear_list = keyword_list[2]
angry_list = keyword_list[3]
disgust_list = keyword_list[4]
surprise_list = keyword_list[5]
anticipation_list = keyword_list[6]
acceptance_list = keyword_list[7]


joy_list_emo = emoji_list[0]+icon_list[0]
sadness_list_emo = emoji_list[1]+icon_list[1]
fear_list_emo = emoji_list[2]+icon_list[2]
angry_list_emo = emoji_list[3]+icon_list[3]
disgust_list_emo = emoji_list[4]+icon_list[4]
surprise_list_emo = emoji_list[5]+icon_list[5]
anticipation_list_emo = emoji_list[6]+icon_list[6]
acceptance_list_emo = emoji_list[7]+icon_list[7]


data = CSVExecutor.read_csv(path='Dataset/train_NSC.csv')
for idx, inst in enumerate(data):
    if len(inst) != 1:
        temp = []
        temp.append(inst[0])
        if rulebase.check_emo_in_word(joy_list, joy_list_emo, inst[0]):
            temp.append('joy')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(sadness_list, sadness_list_emo, inst[0]):
            temp.append('sadness')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(fear_list, fear_list_emo, inst[0]):
            temp.append('fear')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(angry_list, anticipation_list_emo, inst[0]):
            temp.append('anger')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(disgust_list, disgust_list_emo, inst[0]):
            temp.append('disgust')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(surprise_list, surprise_list_emo, inst[0]):
            temp.append('surprise')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(anticipation_list, anticipation_list_emo, inst[0]):
            temp.append('anticipation')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(acceptance_list, acceptance_list_emo, inst[0]):
            temp.append('acceptance')
        else:
            temp.append('')
        predict = rulebase.check_emo(temp)
        emo_predict = ''
        for stm in predict[1:]:
            if stm != '':
                emo_predict = stm
                break
        if inst[9] != '':
            emo_default = ''
            if int(inst[9]) == 1:
                for stm in inst[1:9]:
                    if stm != '':
                        emo_default = stm
                        break
            elif int(inst[9]) == 4:
                for stm in predict[1:]:
                    if stm != '':
                        emo_default = stm
                        break
            else:
                emo_default = rulebase.get_emo(int(inst[10]))
            if emo_default != '':
                if emo_default != emo_predict:
                    data[idx][9] = 0
                    data[idx][10] = rulebase.revert_emo_to_number(emo_default)
                else:
                    data[idx][9] = 1
                    data[idx][10] = rulebase.revert_emo_to_number(emo_default)
            data[idx][1:9] = predict[1:]

CSVExecutor.write_csv(path='output/label_fix.csv', data=data)
