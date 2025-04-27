import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.metrics import f1_score
from sklearn import metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: python3 Tree.py <train_file> <test_file>')
    df_train = pd.read_csv(sys.argv[1])
    df_test = pd.read_csv(sys.argv[2])

    header = list(df_train.columns)
    header.remove('knight')

    X_train = df_train.drop('knight', axis='columns')
    y_train = df_train['knight']
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.143, random_state=42, stratify=y_train) 

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.fit_transform(X_val)
    X_test = scaler.fit_transform(df_test)

    myTree = DecisionTreeClassifier()
    myTree = myTree.fit(X_train,y_train)
    prediction = myTree.predict(X_val)

    plot_tree(myTree, filled=True, feature_names=header, class_names=['Jedi', 'Sith'])
    plt.savefig('tree.png', dpi=300)
    print('F1Score : ' + str(f1_score(y_val, prediction, average='micro')))
    
    prediction = myTree.predict(X_test)
    np.savetxt('Tree.txt', prediction, fmt='%s')

