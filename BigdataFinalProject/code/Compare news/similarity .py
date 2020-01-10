import requests
import json, sys
import pymongo
import pandas as pd

mongo_url = "127.0.0.1:27017"

client = pymongo.MongoClient(mongo_url)

database = "bigdata"
db = client[database]

collection = "news_data"
db_coll = db[collection].find(no_cursor_timeout=True)
text2 = ""
target = 15
result_list = list()
text1 = db_coll[target]['text']
url1 = db_coll[target]['url']
url_list = list()
def get_data(url,post_data):
    req = requests.post(url=url, json=post_data)
    if req.status_code ==200:
        return req.json()

for i, data in enumerate(db_coll):
    if i != target:
        text2 = data['text']
        post_data = {
            "text1": text1,
            "text2": text2,
            "apiKey": "4377299f-ecfe-4c58-9a0f-1785be544f82",
        }
        url = "http://analytics.eventregistry.org/api/v1/semanticSimilarity"
        jsonData =get_data(url,post_data)
        if 'url' in data.keys() and 'similarity' in jsonData.keys():
            if data['url'] not in url_list:
                result = {'similarity': jsonData['similarity'], 'url': data['url']}
                result_list.append(result)
                url_list.append(data['url'])

db_coll.close()
result_list.sort(key=lambda k: k['similarity'], reverse=True)
for l in result_list[:5]:
    print(l)

