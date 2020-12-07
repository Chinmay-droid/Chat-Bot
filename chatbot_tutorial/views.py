from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
from .chatter import response
from .cosine_similarity import get_similar_questions
from .bert import get_bert_similarity
from .lda import get_most_similar_documents
greeting = None
user_class = None

def chat(request):
    context = {}
    return render(request, 'chatbot_tutorial/chatbot.html', context)


def respond_to_websockets(message):
    result_message = {
        'type': 'text'
    }
    answer = ''
    technical_answer = ''
    result_message['text'] = 'Our Training Manager will get back to you'
    
    global greeting
    if not greeting:
        answer = response(message['text'])
        if answer:
            result_message['text'] =  answer
            greeting = 'done'
            return result_message
    global user_class
    if not user_class:
        result_message['text'] = "In which FLOSS you are having a doubt"
        user_class = '1'
    elif "floss" in message['text'].lower():
        result_message['text'] = "Ok We've noted that. \n Please ask your question ..."
        the_class = message['text'].split('floss')[0]
        user_class = the_class
    else:
        # cosine simi;arity
        technical_answer = get_similar_questions(message['text'],user_class)
        #BERT
        #technical_answer = get_bert_similarity(message['text'],user_class)
        #LDA
        #technical_answer = get_most_similar_documents(message['text'],user_class)
        if technical_answer:
            result_message['text'] = technical_answer
    return result_message


    
