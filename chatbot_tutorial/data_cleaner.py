import re
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
sw = stopwords.words('english')

def prettify(string):
    string = string.lower()
    string = string.replace('-', ' ')
    string = string.strip()
    string = string.replace(' ', '-')
    string = re.sub('[^A-Za-z0-9\-]+', '', string)
    string = re.sub('-+', '-', string)
    return string


def pre_process(text):

    text=text.lower()                       # lowercase
    text=re.sub("<!--?.*?-->","",text)      # remove tags
    text=re.sub("(\\d|\\W)+"," ",text)      # remove special characters and digits
    return text

def clean_user_data(text):
    words = word_tokenize(pre_process(text.lower()))
    clean_list = [w for w in words if not w in sw]
    return clean_list
