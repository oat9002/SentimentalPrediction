import CSVExecutor
import WordExecutor

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
# print(joy_list, sadness_list, fear_list, angry_list, disgust_list, surprise_list, anticipation_list, acceptance_list)
