import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('../Train_knight.csv')
    df.loc[df['knight'] == 'Jedi', 'knight'] = 1
    df.loc[df['knight'] == 'Sith', 'knight'] = -1
    correlation = df.corr()
    sns.heatmap(correlation)
    # plt.show()
    plt.savefig('heatmap.jpg')
    # TODO check values of correlation