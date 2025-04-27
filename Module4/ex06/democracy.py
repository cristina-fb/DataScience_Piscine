from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import f1_score
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 KNN.py <train_file> <test_file>')
    df_train = pd.read_csv(sys.argv[1])
    df_test = pd.read_csv(sys.argv[2])
    header = list(df_train.columns)
    header.remove('knight')

    X_train = df_train.drop('knight', axis='columns')
    y_train = df_train['knight']
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=42, stratify=y_train)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.fit_transform(X_val)
    X_test = scaler.fit_transform(df_test)

    tree = DecisionTreeClassifier()
    knn = KNeighborsClassifier(n_neighbors=4)
    log = LogisticRegression()

    estimators=[('Tree', tree), ('KNN', knn), ('Log Reg', log)]
    voting_clf_hard = VotingClassifier(estimators=estimators, voting='hard')
    voting_clf_hard.fit(X_train, y_train)
    prediction = voting_clf_hard.predict(X_val)

    print('F1Score : ' + str(f1_score(y_val, prediction, average='micro')))

    prediction = voting_clf_hard.predict(X_test)
    np.savetxt('Voting.txt', prediction, fmt='%s')