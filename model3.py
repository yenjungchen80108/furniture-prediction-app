import pandas as pd
from sklearn import preprocessing
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
#read in furniture file
dfOld = pd.read_csv('C:/Users/emily/Desktop/blog/furniture/furniture.csv',sep=",",
                  names=['item_id','name','category','old_price','sellable_online','link','other_colors'
                ,'short_description','designer','depth','height','width','price'],skiprows=1, header=None)
#include 7 features
include = ['category','sellable_online','other_colors','depth','height','width','price']
df = dfOld[include]
#replaced the missing values with the mode value in that column
col_names = df.columns  
for c in col_names: 
    df = df.replace("?", np.NaN) 
df = df.apply(lambda x:x.fillna(x.value_counts().index[0]))
#convert categorical values to numerical ones
cat_col=['category','sellable_online','other_colors']
labelEncoder = preprocessing.LabelEncoder()   
mapping_dict ={} 
for col in cat_col: 
    df[col] = labelEncoder.fit_transform(df[col]) 
    le_name_mapping = dict(zip(labelEncoder.classes_,labelEncoder.transform(labelEncoder.classes_))) 
    mapping_dict[col]= le_name_mapping 
print(mapping_dict)
# extract data for fitting
X = df.drop('price', axis=1)  # features
y = df['price'] # labels 
# split the data into training and test data sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=100)
dt = DecisionTreeRegressor()
dt.fit(X_train, y_train)
#print("Prediction:",dt.predict(X_test))
# Saving model to disk
pickle.dump(dt, open('model.pkl','wb'))
# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
#print(model.predict(X_test))