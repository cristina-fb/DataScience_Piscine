import sys
import seaborn as sns
import matplotlib.pyplot as plt
from tabulate import tabulate
from sklearn import metrics

def confusion_matrix(truth, predictions):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for t, p in zip(truth, predictions):
        if t == p and t == "Jedi":
            TN += 1
        elif t == p and t == "Sith":
            TP += 1
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

    sns.heatmap(data=[[TN, FP], [FN, TP]], cmap="Spectral", annot=True)
    plt.savefig('confusion_matrix.png', dpi=300)

    print(tabulate([['Jedi', precisionN, recallN, f1N, TN+FP ], ['Sith', precisionP, recallP, f1P, TP+FN], ['Accuracy', None, None, accuracy, TN+FN+TP+FP]], headers=['', 'Precision', 'Recall', 'F1', 'Total']))
    print()
    print([[TN, FP], [FN, TP]])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 Confusion_Matrix.py <truth> <predictions>")
        sys.exit(1)

    truth = open(sys.argv[1], "r")
    truth = truth.read()
    truth = truth.split("\n")

    predictions = open(sys.argv[2], "r")
    predictions = predictions.read()
    predictions = predictions.split("\n")

    confusion_matrix(truth, predictions)