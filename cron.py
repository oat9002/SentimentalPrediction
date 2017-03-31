# -*- coding: utf-8 -*-
import time
from pymongo import MongoClient
from datetime import datetime, timedelta
# import model
import rulebase 
import CSVExecutor
import WordExecutor
import requests
import schedule
import uuid
import random
import json

client = MongoClient('mongodb://10.0.1.3:27017/')
db = client['SocialData']
tweet_collection = db.tweet
predicted_collection = db.predicted
predicted_tweets_collection = db.predicted_tweets

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

def summarize(data, pred_list):
    result = []
    for i in data:
        temp = {}
        key = list(i.keys())[0];
        total = len(i[key])
        if total != 0: 
            temp['joy'] = format((i[key].count(1) / total) * 100, '.2f')
            temp['sadness'] = format((i[key].count(2) / total) * 100, '.2f')
            temp['fear'] = format((i[key].count(3) / total) * 100, '.2f')
            temp['anger'] = format((i[key].count(4) / total) * 100, '.2f')
            temp['disgust'] = format((i[key].count(5) / total) * 100, '.2f')
            temp['surprise'] = format((i[key].count(6) / total) * 100, '.2f')
            temp['anticipation'] = format((i[key].count(7) / total) * 100, '.2f')
            temp['acceptance'] = format((i[key].count(8) / total) * 100, '.2f')
        else:
            temp['joy'] = format(0, '.2f')
            temp['sadness'] = format(0, '.2f')
            temp['fear'] = format(0, '.2f')
            temp['anger'] = format(0, '.2f')
            temp['disgust'] = format(0, '.2f')
            temp['surprise'] = format(0, '.2f')
            temp['anticipation'] = format(0, '.2f')
            temp['acceptance'] = format(0, '.2f')
        geolocation = requests.get('http://localhost:5005/place', {'place_id': key}).json()['place']['geolocation']
        geolocation = geolocation.split(',')
        temp['latitude'] = float(geolocation[0])
        temp['longitude'] = float(geolocation[1])
        max_emo_list = find_summarize_max_emo(temp)
        temp['max_emo'] = pickMaxEmo(max_emo_list)
        temp['predicted_texts'] = predicted_text_summarize(max_emo_list, pred_list, key)
        result.append(temp)
    return result

def pickMaxEmo(max_emo_list):
    rand = random.randint(0, len(max_emo_list) - 1)
    return max_emo_list[rand]

def find_summarize_max_emo(summarize_data):
    max_val = 0.0
    max_emo_list = []
    key_list = list(summarize_data.keys())
    key_list.remove('latitude')
    key_list.remove('longitude')
    for key in key_list:
        if max_val < float(summarize_data[key]):
            max_val = float(summarize_data[key])
    for key in key_list:
        if max_val - float(summarize_data[key]) < 0.00001:
            max_emo_list.append(rulebase.revert_emo_to_number(key))
    return max_emo_list

def predicted_text_summarize(max_emo_list, pred_list, place_id):
    all_texts = []
    selected_texts = []
    for max_emo in max_emo_list:
        for tw in pred_list:
            if place_id == tw[1]:
                if max_emo == tw[0]:
                    all_texts.append(tw[2])
    all_texts = list(set(all_texts))
    if len(all_texts) > 3:
        for i in range(0, 3):
            rand = random.randint(0, len(all_texts) - 1)
            selected_texts.append(all_texts[rand])
            all_texts.remove(all_texts[rand])
    else:
        for i in range(0, len(all_texts)):
            rand = random.randint(0, len(all_texts) - 1)
            selected_texts.append(all_texts[rand])
            all_texts.remove(all_texts[rand])
    return list(set(selected_texts))

def predict_cron():
    # start = datetime.today().replace(hour=0,minute=0,second=0, microsecond=0)
    start = (datetime.now() - timedelta(hours=3))
    start = start - timedelta(hours=7)
    end = datetime.today()
    end = end - timedelta(hours=7)
    tweets = requests.get('http://localhost:5005/tweet/date?start=' + str(start) + '&end=' + str(end))
    pred_list = []
    for tw in tweets.json()['tweets']:
        temp = []
        pred = []
        emo_count = []
        temp.append(tw['text'])
        if rulebase.check_emo_in_word(joy_list,joy_list_emo, tw['text'], emo_count):
            temp.append('joy')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(sadness_list,sadness_list_emo, tw['text'], emo_count):
            temp.append('sadness')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(fear_list,fear_list_emo, tw['text'], emo_count):
            temp.append('fear')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(anger_list,anger_list_emo, tw['text'], emo_count):
            temp.append('anger')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(disgust_list,disgust_list_emo, tw['text'], emo_count):
            temp.append('disgust')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(surprise_list,surprise_list_emo, tw['text'], emo_count):
            temp.append('surprise')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(anticipation_list,anticipation_list_emo, tw['text'], emo_count):
            temp.append('anticipation')
        else:
            temp.append('')
        if rulebase.check_emo_in_word(acceptance_list,acceptance_list_emo, tw['text'], emo_count):
            temp.append('acceptance')
        else:
            temp.append('')
        pred.append(rulebase.get_predicted(rulebase.check_emo(temp, emo_count)))
        pred.append(tw['place_id'])
        pred.append(tw['text'])
        pred.append(tw['id'])
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
    predicted = summarize(place_with_pred, pred_list)
    predicted_id = str(uuid.uuid4())
    # predicted_collection.insert_one({'id': predicted_id, 'predicted': predicted}).inserted_id
    r = requests.post('http://localhost:5005/predicted/save', data = json.dumps({'id': predicted_id, 'predicted': predicted}))
    

schedule.every(5).minutes.do(predict_cron)
while True:
    schedule.run_pending()
    time.sleep(1)
    # testset = WordExecutor.to_scikitlearn_dataset(data=freq_test, attribute=sorted(u))
    # pred_list = clf.predict(testset)
    # print(pred_list)
# if __name__ == '__main__':
#     predict_cron()
# start = datetime.datetime(2017, 2, 1)
# end = datetime.datetime(2017, 2, 2)

# test = tweet.find({"created_at": {"$gte": start, "$lte": end}})
# for i in test:
#     print(i.keys())