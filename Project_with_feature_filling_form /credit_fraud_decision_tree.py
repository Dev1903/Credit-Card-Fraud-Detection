
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
credit=pd.read_csv('creditcard.csv')
credit

X=credit.drop(['Class','Amount','Time'], axis=1)
Y=credit['Class']

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.2)
# print('Training Data',X_train)
# print('Testing Data',X_test)
# print('Training Data y',y_train)
# print('Testing Data y',y_test)

from sklearn.tree import DecisionTreeClassifier
classifier=DecisionTreeClassifier()
classifier.fit(X_train,y_train)

y_pred=classifier.predict(X_test)
# y_pred

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(y_test,y_pred))
print(classification_report(y_test,y_pred, target_names=['FAKE','AUTHENTIC']))
def detect_fraud(features):
    # Your existing fraud detection logic here
    y_pred=classifier.predict([features])
    print(y_pred)
    if(y_pred == 1):
        return("The Credit Card is authentic")
    else:
        return("The Credit Card is fake")



