# -*- coding: utf-8 -*-
"""
Created on Wed Jul 08 02:43:08 2020

@author: Olawuyi Feyisola
"""
from data import *

import pandas as pd

df = pd.read_csv('csv/business.csv')
df.head()
df.describe()

# select company as new feature (performance eval)
features = df[['industry', 'product-service', 'rating']].values

from sklearn import preprocessing

# Preprocessing Multi class features in data
industry = preprocessing.LabelEncoder()
industry.fit(ind)
features[:, 0] = industry.transform(features[:, 0])

service = preprocessing.LabelEncoder()
service.fit(srvc)
features[:, 1] = service.transform(features[:, 1])


labels = df['social-media']

from sklearn.model_selection import train_test_split

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.3,
                                                                            random_state=5)

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=1000, random_state=42)
rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)


def predict(industry, service, rating):
    industries_encode = ind_enc
    if any(industry in x for x in industries_encode):
        result_0 = [x for x in industries_encode if x[0] == industry]
        encode_0 = result_0[0][1]
        # print(encode_0)
    else:
        raise Exception("Wrong Industry Input")

    services_encode = srvc_enc
    if any(service in x for x in services_encode):
        result_1 = [x for x in services_encode if x[0] == service]
        encode_1 = result_1[0][1]
        # print(encode_0)
    else:
        raise Exception("Wrong Service Input")

    test = [[encode_0, encode_1, rating]]
    prediction = rf.predict(test)
    recommended = prediction[0]
    return recommended


# Content-Based Recommender - TF-IDF; Cosine similarity
socials_df = pd.read_csv('csv/socials.csv')
from sklearn.feature_extraction.text import TfidfVectorizer

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(socials_df['type'])
from sklearn.metrics.pairwise import linear_kernel

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
recommender_results = {}
for index, row in socials_df.iterrows():
    similar = cosine_similarities[index].argsort()[:-5:-1]
    similar_socials = [(cosine_similarities[index][i], socials_df['id'][i]) for i in similar]
    recommender_results[row['id']] = similar_socials[1:]


def item(id):
    return socials_df.loc[socials_df['id'] == id]['social-media'].tolist()[0]


def predictSimilar(platform):
    # convert platform to platform_id
    platform_encode = [['Pinterest', 1], ['Twitter', 2], ['Instagram', 3], ['Linkedin', 4], ['Facebook', 5],
                       ['Snapchat', 6], ['Youtube', 7], ['Tumblr', 8], ['Tiktok', 9], ['Medium', 10], ['Spotify', 11],
                       ['Behance', 12], ['Github', 13], ['ResearchGate', 14], ['Reddit', 15]]
    if any(platform in x for x in platform_encode):
        result_2 = [x for x in platform_encode if x[0] == platform]
        id = result_2[0][1]
        # print(id)
    else:
        raise Exception("Wrong input")

    res = recommender_results[id][:3]
    test_result = {0: {platform}}
    i = 1
    for r in res:
        test_result[i] = {item(r[1])}
        i = i + 1
    return test_result



# recommend("Fashion", "Fashion retail", "Adults", 5)
# recommend("Information Communication Technology", "Mobile software development", 5)
# recommend("Artificial Intelligence", "Data science", 5)
