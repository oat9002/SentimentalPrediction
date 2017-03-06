# -*- coding: utf-8 -*-
from pymongo import MongoClient
from datetime import datetime, timedelta
# import model
import rulebase 
import CSVExecutor
import WordExecutor
import requests
import schedule
import time

client = MongoClient('mongodb://10.0.1.3:27017/')
db = client['SocialData']
tweet_collection = db.tweet
predicted_collection = db.predicted

# library = CSVExecutor.read_csv('./Dataset/8EMO_label.csv')
# words = []
# for li in library:
#     words.append(li[0])
# unigram = WordExecutor.create_ngram_from_list_bynltk(words, 1)
# u = WordExecutor.remove_strange_word_and_normalize(unigram)
# clf = model.read_model_scikitlearn('./output/model.pkl')

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

joy_list_emo = emoji_list[0]+icon_list[0]
sadness_list_emo = emoji_list[1]+icon_list[1]
fear_list_emo = emoji_list[2]+icon_list[2]
anger_list_emo = emoji_list[3]+icon_list[3]
disgust_list_emo = emoji_list[4]+icon_list[4]
surprise_list_emo = emoji_list[5]+icon_list[5]
anticipation_list_emo = emoji_list[6]+icon_list[6]
acceptance_list_emo = emoji_list[7]+icon_list[7]

def summarize(data):
    result = []
    for i in data:
        temp = {}
        key = ''
        for d in i.keys():
            key = d
        total = len(i[key])
        temp['joy'] = format((i[key].count(1) / total) * 100, '.2f')
        temp['sadness'] = format((i[key].count(2) / total) * 100, '.2f')
        temp['fear'] = format((i[key].count(3) / total) * 100, '.2f')
        temp['anger'] = format((i[key].count(4) / total) * 100, '.2f')
        temp['disgust'] = format((i[key].count(5) / total) * 100, '.2f')
        temp['surprise'] = format((i[key].count(6) / total) * 100, '.2f')
        temp['anticipation'] = format((i[key].count(7) / total) * 100, '.2f')
        temp['acceptance'] = format((i[key].count(8) / total) * 100, '.2f')
        geolocation = requests.get('http://localhost:5005/place', {'place_id': key}).json()['place']['geolocation']
        geolocation = geolocation.split(',')
        temp['latitude'] = float(geolocation[0])
        temp['longitude'] = float(geolocation[1])
        result.append(temp)
    return result
    

def predict_cron():
    # start = datetime.today().replace(hour=0,minute=0,second=0, microsecond=0)
    start = (datetime.now() - timedelta(days = 1)).replace(hour=0,minute=0,second=0, microsecond=0)
    end = datetime.today().replace(hour=23,minute=59,second=59, microsecond=999999)
    tweets = tweet_collection.find({"created_at": {"$gte": start, "$lte": end}})
    pred_list = []
    for tw in tweets:
        temp = []
        pred = []
        temp.append(tw['text'])
        if rulebase.check_emo_in_word(joy_list,joy_list_emo, tw['text']):
            temp.append('joy')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(sadness_list,sadness_list_emo, tw['text']):
            temp.append('sadness')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(fear_list,fear_list_emo, tw['text']):
            temp.append('fear')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(anger_list,anger_list_emo, tw['text']):
            temp.append('anger')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(disgust_list,disgust_list_emo, tw['text']):
            temp.append('disgust')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(surprise_list,surprise_list_emo, tw['text']):
            temp.append('surprise')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(anticipation_list,anticipation_list_emo, tw['text']):
            temp.append('anticipation')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(acceptance_list,acceptance_list_emo, tw['text']):
            temp.append('acceptance')
        else:
            temp.append('')
        pred.append(rulebase.get_predicted(rulebase.check_emo(temp)))
        pred.append(tw['place_id'])
        pred_list.append(pred)
    place = []
    for p in pred_list:
        place.append(p[1])
    place = list(set(place))
    place_with_pred = []
    for p in place:
        temp = {}
        temp[p] = []
        for i in pred_list:
            if p == i[1]:
                temp[p].append(i[0]) 
        place_with_pred.append(temp)
    predicted_collection.insert_one({'predicted': summarize(place_with_pred)}).inserted_id

schedule.every(3).minutes.do(predict_cron)
while True:
    schedule.run_pending()
    time.sleep(1)
    # testset = WordExecutor.to_scikitlearn_dataset(data=freq_test, attribute=sorted(u))
    # pred_list = clf.predict(testset)
    # print(pred_list)

# start = datetime.datetime(2017, 2, 1)
# end = datetime.datetime(2017, 2, 2)

# test = tweet.find({"created_at": {"$gte": start, "$lte": end}})
# for i in test:
#     print(i.keys())