'''
Author - Utkarsh
Date - 30-10-2020 

This code gets the unique keywords and creates a dataframe with the original slide name and
the keywords as separate columns. In each of these keyword columns, there are 1's and 0's. If
a keyword is present in that particular slide, the corresponding column of that keyword has 
1 otherwise 0 in that slide row.

The final dataframe is data.

'''

import pandas as pd
import re

def find_word(text, search):
   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False

data = pd.read_excel(r'data\creation_tutorialcommoncontent-2020-10-11-13-10-57.xlsx')


cols = [data.columns[1],data.columns[2],data.columns[14]]
data = pd.DataFrame(data=data[cols])

keywords = data['keyword']

kw = []
for i in keywords.index:
    l = keywords.loc[i]
    l = l.split(',')
    kw.extend(l)

for i in range(0,len(kw)):
    kw[i] = kw[i].strip()
    if kw[i][-1] == '.':
        kw[i] = kw[i].replace('.','')
    if len(kw[i].split('.')) >= 2:
        x = []
        for j in range(1,len(kw[i].split('.'))):
            x.append(kw[i].split('.')[j].strip())
        kw[i] = kw[i].split('.')[0].strip()
        kw.extend(x)
        
kw = list(set(kw))

for i in kw:
    data[i] = 0
    for j in data.index:
        if find_word(data.loc[j,'keyword'],i):
            data.loc[j,i] = 1

