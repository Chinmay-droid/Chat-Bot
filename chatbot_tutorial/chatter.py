import re
import random
import string

#WordNetLemmatizer - LemmatizeWords to RemovePunctuations
#BeautifulSoup

def name_extract(text):
  text = text.lower()
  name_found = ''
  if 'my name is' in text:
    x = text.split('my name is ')
    y = x[-1]
    z = y.split(' ')
    name_found = z[0]
  elif 'i am' in text:
    x = text.split('i am ')
    y = x[-1]
    z = y.split(' ')
  elif "i'm" in text:
    x = text.split("i'm ")
    y = x[-1]
    z = y.split(' ')
    name_found = z[0]
  elif 'myself' in text:
    x = text.split('myself ')
    y = x[-1]
    z = y.split(' ')
    name_found = z[0]
  else:
    x = text.split(' ')
    y = x[0]
    name_found = y
  return name_found

def response(text):
  response =  ''
  name ='user'

  welcome_responses = {
      'Hi': ["Hello there, how can I help you?" , "Hi! please ask your question!", "Hello! Please ask me your doubt."],
      'Hi_name' : [str("Hello "+ name +", how can I help you?"), str("Glad to meet you "+ name +", please ask your question.")]      
  }

  closing_responses = {
      'Thanks' : ['You are welcome !','You are welcome, I am always there to help!','You are welcome! Ping me if you need anything else here'],   
      'understood_thanks' : ['Great that you understood..You are always welcome!','It is good to know that you got it. You are always welcome!', 'Great that it is solved..You are always welcome!','It is good to know that it worked. You are always welcome!','That is great. Ask me anything whenever you need!']  
  }

  w1 = re.search('Hi',text,re.IGNORECASE)

  w2 = re.search('hey',text,re.IGNORECASE)
  w3 = re.search('hello',text,re.IGNORECASE)

  c1 = re.search('thanks+',text,re.IGNORECASE)
  c2 = re.search('thank+',text,re.IGNORECASE)
  c3 = re.search('understood|got it|solved',text) 

  n1 = re.search('my name is+',text,re.IGNORECASE)
  n2 = re.search('I am+',text,re.IGNORECASE)
  n3 = re.search('myself+',text,re.IGNORECASE)
  n4 = re.search("I'm ", text, re.IGNORECASE)

  if w1 or w2 or w3:
    if n1 or n2 or n3 or n4:
      name = name_extract(text)
      name = name[0:1].upper()+name[1:]
      response = random.choice(welcome_responses['Hi_name'])
      response = response.replace('user',name)
    else:
      response = random.choice(welcome_responses['Hi'])  
  elif c1 or c2:
    if c3:
      response =  random.choice(closing_responses['understood_thanks'])
    else:
      response = random.choice(closing_responses['Thanks'])
  elif n1 or n2 or n3 or n4:
    name = name_extract(text)
    name = name[0:1].upper()+name[1:]
    response = random.choice(welcome_responses['Hi_name'])
    response = response.replace('user',name)
  elif c3:
    response =  random.choice(closing_responses['understood_thanks'])

  return response