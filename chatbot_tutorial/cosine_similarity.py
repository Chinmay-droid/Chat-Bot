#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 09:13:34 2020

@author: saurabhadhikary
"""
import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
sw = stopwords.words('english')
from .data_cleaner import pre_process
import pandas as pd
import os

def cos_get(data, user_ques):
    total = []
    l1 = []
    l2 = []
    ques = word_tokenize(pre_process(data))
    total = user_ques + ques

    for w in total: 
        if w in user_ques: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in ques: l2.append(1) 
        else: l2.append(0)        
    cs = cosine_similarity((l1,l2))
    return cs[0][1] # return a matrix

def get_similar_questions(user_ques,q_class):
    q_class = str(q_class).lower().strip()
    df = pd.read_csv(os.getcwd()+'/chatbot_tutorial/data/complete_df.csv')
    df = df[df.keyword.str.contains(str(q_class),na=False,regex=True)]
    user_ques = word_tokenize(pre_process(user_ques))
    user_ques =[w for w in user_ques if not w in sw]
    df['cos'] = df['parsed_title'].apply(lambda x:cos_get(x,user_ques) )
    df = df.sort_values('cos',ascending=False)
    df = df.query('cos>0.7')
    output = df[:1]
    print("&^&^&^",df,"^^"*20,output,len(output),'*********\n\n\n')
    if len(output):
        return output['parsed_body_ans'].values[0]
    else:
        return None

print("similarity :\n\n\n",get_similar_questions('color of plot','Python'))