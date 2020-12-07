# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 18:16:46 2020

@author: Utkarsh 

The function "parse_this" parses the body and title (if present) of the questions and answers.
It removes various html tags in the actual text of the body and also removes any unnecessary spaces
in the beginning and at last of the text.
Currently, I am keeping the original text of the title and the body. I am adding the cleaned text 
in separate columns of the dataframe preixed by "parsed_".

"""

import pandas as pd
from bs4 import BeautifulSoup
import unicodedata

def parse_this(filepath):
    d = pd.read_csv(filepath)
    t = d.loc[:,'body']
    if 'title' in d.columns:
        d['parsed_title'] = 0
    d['parsed_body'] = 0
    for i in range(len(t)):
        print("i :",i)
        s = BeautifulSoup(t[i],'html.parser')
        d.loc[i,'parsed_body'] = unicodedata.normalize("NFKD",s.get_text(strip=True).strip())
        if 'title' in d.columns:
            d.loc[i,'parsed_title'] = d.loc[i,'title'].strip()
        d.loc[i,'parsed_body'] = d.loc[i,'parsed_body'].replace(u'\xa0',u'')
        d.loc[i,'parsed_body'] = d.loc[i,'parsed_body'].replace(u'\r\n',u'')
        d.loc[i,'parsed_body'] = d.loc[i,'parsed_body'].replace(u'\n\n',u'')
        d.loc[i,'parsed_body'] = d.loc[i,'parsed_body'].replace(u"!@#$%^&*()[]{};:,./<>?\|`~-=_+",u'')
    return d

def parser(filepath):
  d = pd.read_csv(filepath)
  for col in d.columns:
    if col in ('title','body'):
      parsed_col = 'parsed_'+str(col)
      
      d[parsed_col] = d[col].str.strip()
      d[parsed_col] = d[parsed_col].replace(u'\xa0',u'',regex=True)
      d[parsed_col] = d[parsed_col].replace(u'\n\n',u'',regex=True)
      d[parsed_col] = d[parsed_col].replace(u'\r\n',u'',regex=True)
      d[parsed_col] = d[parsed_col].replace(u"!@#$%^&*()[]{};:,./<>?\|`~-=_+",u'')
      d[parsed_col] = d[parsed_col].str.lower().map(
          lambda x: unicodedata.normalize('NFKD', BeautifulSoup(str(x),'html.parser').getText()))
  return d
 
ques_PATH = r'data/website_question.csv'
questions_cleaned = parser(ques_PATH)

ans_PATH = r'data/website_answer.csv'
answers_cleaned = parser(ans_PATH)

df_merge_q_a = pd.merge(questions_cleaned,
                answers_cleaned, left_on='id', right_on='question_id',how='inner',
                suffixes=('_ques','_ans'))
q_a_keys = ['question_id','parsed_title','parsed_body_ques',
            'parsed_body_ans','category','tutorial']
q_a_df = df_merge_q_a[q_a_keys]
#print("done",q_a_df)

tutorial_PATH = r'data/tutorials.csv'
tutorials_cleaned = parser(tutorial_PATH)
tutorials_cleaned['tutorial'] = tutorials_cleaned['tutorial'].str.strip()
tutorials_cleaned['tutorial'] = tutorials_cleaned.tutorial.replace(' ','-',regex=True)
df_merge_q_a_t = pd.merge(q_a_df,
                  tutorials_cleaned, on='tutorial',how='outer',
                  suffixes=('_ques','_tut'))

df_merge_q_a_t = df_merge_q_a_t[q_a_keys]
df_merge_q_a_t = df_merge_q_a_t.query('parsed_title == parsed_title')
df_merge_q_a_t.to_csv('df_merge_q_a_t.csv')

common_content_PATH = r'data/class.csv'
common_content_cleaned = parser(common_content_PATH)
common_content_cleaned['slide'] = common_content_cleaned['slide'].replace('-Slides.zip','',regex=True)


df_merge_q_a_t_c = pd.merge(df_merge_q_a_t,
                  common_content_cleaned, left_on ='tutorial',right_on='slide' , how='outer',
                  suffixes=('_ques','_tut'))

q_a_keys = ['question_id','parsed_title','parsed_body_ques',
            'parsed_body_ans','category','tutorial','keyword']

complete_df = df_merge_q_a_t_c[q_a_keys]
complete_df = complete_df.query('parsed_title == parsed_title')

complete_df.to_csv('data/complete_df.csv')


#print(complete_df)



