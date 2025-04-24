import sys
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

def get_f1score(truth, predictions):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for t, p in zip(truth, predictions):
        if t == p and t == "Jedi":
            TP += 1
        elif t == p and t == "Sith":
            TN += 1
        elif t != p and t == "Jedi":
            FP += 1
        elif t != p and t == "Sith":
            FN += 1

    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precisionP = TP / (TP + FP)
    precisionN = TN / (TN + FN)
    recallP = TP / (TP + FN)
    recallN = TN / (TN + FP)
    f1P = 2 * (precisionP * recallP) / (precisionP + recallP)
    f1N = 2 * (precisionN * recallN) / (precisionN + recallN)
    print('F1Score Jedi: ' + str(f1P))
    print('F1Score Sith: ' + str(f1N))

def get_train_test(df_train):
    X = df_train.drop('knight', axis='columns')
    y = df_train['knight']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.143, random_state=42, stratify=y) #14.3% of 70% training (10% of total)
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 KNN.py <train_file> <test_file>')
    df_train = pd.read_csv(sys.argv[1])
    df_test = pd.read_csv(sys.argv[2])
    header = list(df_train.columns)
    header.remove('knight')
    X_train, X_test, y_train, y_test = get_train_test(df_train)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    prediction = knn.predict(X_test)

    np.savetxt('KNN.txt', prediction, fmt='%s')

    truth = open('../truth.txt', 'r')
    truth = truth.read()
    truth = truth.split("\n")
    get_f1score(truth, prediction)