import pandas as pd
import os 

data=pd.read_csv(os.getcwd()+'/chatbot_tutorial/data/small_df.csv')
data.head()

import BERTSimilarity.BERTSimilarity as bertsimilarity
bertsimilarity=bertsimilarity.BERTSimilarity()

#Function to find similarity between the sentences/paragraphs
def calculate_similarity(q1,q2,bertsimilarity):
    dist=bertsimilarity.calculate_distance(q1,q2)
    return dist
def get_bert_similarity(user_ques,user_class):
	print("BERT similarity running ....")
	q2= user_ques
	distances=[]
	for i in range(len(data[:100])):
	    q1=data['parsed_title'][i]
	    z=calculate_similarity(q1,q2,bertsimilarity)
	    distances.append(z)
	    print(distances)
	result_dataset=pd.DataFrame(columns=['question1','question2','similarity_score','parsed_body_ans'])
	result_dataset['question1']=data['parsed_title'][:100]
	result_dataset['question2']=q2
	result_dataset['similarity_score']=distances
	result_dataset['parsed_body_ans'] = data['parsed_body_ans']
	result_dataset = result_dataset.sort_values('similarity_score',ascending=False)
	result_dataset = result_dataset.query('similarity_score>0.7')
	output = result_dataset[:1]
	print("&^&^&^","^^"*20,output,len(output),'*********\n\n\n')
	print("BERT similarity ended")
	if len(output):
	    return output['parsed_body_ans'].values[0]
	else:
		return None