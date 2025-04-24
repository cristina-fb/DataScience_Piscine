import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('../Train_knight.csv')
    df.loc[df['knight'] == 'Jedi', 'knight'] = 1
    df.loc[df['knight'] == 'Sith', 'knight'] = 0
    correlation = df.corr()
    sns.heatmap(correlation)
    plt.savefig('heatmap.jpg', dpi=300)