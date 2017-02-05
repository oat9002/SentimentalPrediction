import CSVExecutor
import rulebase

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


data = CSVExecutor.read_csv(path='Dataset/2d_label/test.csv')
for idx, inst in enumerate(data):
    if len(inst) != 1:
        temp = []
        temp.append(inst[0])
        if rulebase.check_emo_in_word(joy_list, inst[0]):
            temp.append('joy')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(sadness_list, inst[0]):
            temp.append('sadness')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(fear_list, inst[0]):
            temp.append('fear')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(angry_list, inst[0]):
            temp.append('angry')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(disgust_list, inst[0]):
            temp.append('disgust')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(surprise_list, inst[0]):
            temp.append('surprise')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(anticipation_list, inst[0]):
            temp.append('anticipation')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(acceptance_list, inst[0]):
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
