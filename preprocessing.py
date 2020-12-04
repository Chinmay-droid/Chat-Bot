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
      d[parsed_col] = d[parsed_col].replace(u'\xa0',u'')
      d[parsed_col] = d[parsed_col].replace(u'\r\n',u'')
      d[parsed_col] = d[parsed_col].replace(u'\n\n',u'')
      d[parsed_col] = d[parsed_col].replace(u"!@#$%^&*()[]{};:,./<>?\|`~-=_+",u'')
  return d
    
def get_ques_ans():
  filepath = r'data/questions.csv'
  ques = parse_this(filepath)
  ques = parser(filepath)
  filepath = r'data/website_answer_part.csv'
  ans = parse_this(filepath)
  ans = parser(filepath)
  return ques,ans





