from pprint import pprint

from helper import get_word_count
from idf import get_idf_sentences, get_idf_words
from stringmanip import clean_sentence, get_sentences, get_words
from tf import get_tf_sentences, get_tf_words


def tfidf(paragraph):
	words = get_words(paragraph)
	sentences, len_sentences = get_sentences(paragraph)
	words_count, words_len = get_word_count(words)


	tf_words = get_tf_words(words, words_count, words_len)
	print('TF Words -->')
	print('-'*30)
	pprint(tf_words)
	print('')

	tf_sentences = get_tf_sentences(sentences, tf_words)
	print('TF Sentences -->')
	print('-'*30)
	pprint(tf_sentences)
	print('')


	idf_words = get_idf_words(words, words_count, words_len, len_sentences)
	pprint('IDF Words -->')
	print('-'*30)
	print(idf_words)
	print('')

	idf_sentences = get_idf_sentences(sentences, idf_words)
	pprint('IDF Sentences -->')
	print('-'*30)
	print(idf_sentences)
	print('')

	#Calculating tfidf of each sentence. tfidf = tf*idf
	tfidf = {s:(tf_sentences[s]*idf_sentences[s]) for s in sentences}
	print("\n\n\n\n\n @@@@@@@@@@",tfidf)
	return tfidf
#Sorting the sentences based on their tfidf score.
#Higher the score, more the importance.
# imp_sentences = sorted(tfidf.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
# print('')
# print('Sentences sorted -->')
# print('-'*30)
# pprint(imp_sentences)
