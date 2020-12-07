from preprocessing import get_ques_ans
# pandas
import pandas as pd
# Scikit Learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
# Keras
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding
from tensorflow.keras.layers import LSTM
#Numpy


print("complete_df",complete_df.sort_values(by=['question_id']))
vectorizer = TfidfVectorizer(stop_words='english')
print("complete_df",complete_df.shape)
x_train = vectorizer.fit_transform(complete_df['parsed_title'])
y_train =vectorizer.fit_transform(complete_df['parsed_body_ans'])
x_train.sort_indices()
y_train.sort_indices()
x_train = x_train.toarray()
y_train = y_train.toarray()
print("x_train",x_train[0],'\n',x_train[0].shape,type(x_train[0]))

X_train, X_test, Y_train, Y_test = train_test_split(
	x_train, y_train, test_size=0.2, random_state=42)

# Keras magic
model = Sequential()
model.add(Embedding(20000, 128))
model.add(LSTM(128, dropout=0.33, recurrent_dropout=0.2))
model.add(Dense(372))

model.compile(loss='MeanSquaredLogarithmicError',
              optimizer='adam',
              metrics=['accuracy'])

print("completed\n\n",model,"\n\n",'-------',X_train,X_train.shape,'\n\n',Y_train)

model.fit(X_train,Y_train,
          batch_size=128,
          epochs=1,
          verbose=2,
          validation_data=(X_test,Y_test))

print("over",model)
question = 'Programming language for OpenFOAM.'
# User Input 
user_input = pd.Series([question], index=['text'],dtype="string")
ui_vec = vectorizer.fit_transform(user_input)
user_output = pd.Series(['Nueral Networks helps you remember and predict values based on previous data'], index=['text'],dtype="string")
ui_out =vectorizer.fit_transform(user_output)
ui_vec=sequence.pad_sequences(ui_vec.toarray(),maxlen=372,padding='post')
ui_out=sequence.pad_sequences(ui_out.toarray(),maxlen=372,padding='post')
ev = model.evaluate(ui_vec,ui_out)
pred = model.predict(ui_vec)
print("---",ev,'\n\n',pred)
