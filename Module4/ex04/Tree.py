import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import numpy as np

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
    return f1P, f1N

def plot_tree_graph(model, features):
    plot_tree(model, filled=True, feature_names=features, class_names=['Jedi', 'Sith'])
    plt.savefig('tree.png', dpi=300)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 Tree.py <train_file> <test_file>')
    df_train = pd.read_csv(sys.argv[1])
    df_test = pd.read_csv(sys.argv[2])

    header = list(df_train.columns)
    header.remove('knight')

    X_train = df_train.drop('knight', axis='columns')
    y_train = df_train['knight']
    X_test = df_test.drop('knight', axis='columns') 
    y_test = df_test['knight']

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.fit_transform(X_test)

    myTree = DecisionTreeClassifier()
    myTree = myTree.fit(X_train,y_train)
    prediction = myTree.predict(X_test)

    f1p, f1n = get_f1score(y_test, prediction)
    print('F1Score Jedi: ' + str(f1p))
    print('F1Score Sith: ' + str(f1n))

    plot_tree_graph(myTree, header)
    np.savetxt('Tree.txt', prediction, fmt='%s')
