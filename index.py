# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import json
from pymongo import MongoClient

app = Flask(__name__)

@app.route("/predicted", methods=['GET'])
def get_predicted():
    client = MongoClient('mongodb://10.0.1.3:27017/')
    db = client['SocialData']
    predicted_collection = db.predicted
    predicted = predicted_collection.find().sort("_id", -1).limit(1)
    for p in predicted:
        predicted = p
    del predicted['_id']
    return jsonify(predicted['predicted'])

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5006, threaded=True)
