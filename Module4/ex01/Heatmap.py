import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df = pd.read_csv('../Train_knight.csv')
    df.loc[df['knight'] == 'Jedi', 'knight'] = 0
    df.loc[df['knight'] == 'Sith', 'knight'] = 1
    correlation = df.corr()
    plt.figure(figsize=(10, 10))
    sns.heatmap(correlation)
    plt.savefig('heatmap.jpg', dpi=300)