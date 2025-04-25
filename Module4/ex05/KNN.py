import sys
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def get_accuracy(truth, predictions):
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
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    return accuracy, f1P, f1N

def split_data(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) #14.3% of 70% training (10% of total)
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 KNN.py <train_file> <test_file>')
    df_train = pd.read_csv(sys.argv[1])
    df_test = pd.read_csv(sys.argv[2])
    header = list(df_train.columns)
    header.remove('knight')

    X_train = df_train.drop('knight', axis='columns')
    y_train = df_train['knight']
    # for col in header:
    #     X_train[col] = (X_train[col] - X_train[col].min()) / (X_train[col].max() - X_train[col].min())

    X_train, X_test, y_train, y_test = split_data(X_train, y_train)
    X_train = X_train.reset_index(drop=True)
    X_test = X_test.reset_index(drop=True)
    y_train = y_train.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

    accuracy_plot = []
    for i in range(1,30):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(X_train, y_train)
        prediction = knn.predict(X_test)
        accuracy, f1P, f1N = get_accuracy(y_test, prediction)
        accuracy_plot.append(accuracy)

    plt.plot(range(1,30), accuracy_plot)
    plt.xlabel('k values')
    plt.ylabel('accuracy')
    plt.savefig('KNN.png', dpi=300)

    # For k = 8
    knn = KNeighborsClassifier(n_neighbors=8)
    knn.fit(X_train, y_train)
    prediction = knn.predict(X_test)
    accuracy, f1P, f1N = get_accuracy(y_test, prediction)
    print('F1Score Jedi: ' + str(f1P))
    print('F1Score Sith: ' + str(f1N))
    print('Accuracy: ' + str(accuracy))

    np.savetxt('KNN.txt', prediction, fmt='%s')