import sys
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn import metrics

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

    accuracy_plot = []
    for i in range(1,30):
        knn = KNeighborsClassifier(n_neighbors=i, leaf_size=15)
        knn.fit(X_train, y_train)
        prediction = knn.predict(X_val)
        accuracy_plot.append(accuracy_score(y_val, prediction))

    plt.plot(range(1,30), accuracy_plot)
    plt.xlabel('k values')
    plt.ylabel('accuracy')
    plt.savefig('KNN.png', dpi=300)

    # For k = 4
    knn = KNeighborsClassifier(n_neighbors=4)
    knn.fit(X_train, y_train)
    prediction = knn.predict(X_val)

    print('Accuracy: ' + str(accuracy_score(y_val, prediction)))
    print('F1Score : ' + str(f1_score(y_val, prediction, average='micro')))

    prediction = knn.predict(X_test)
    np.savetxt('KNN.txt', prediction, fmt='%s')