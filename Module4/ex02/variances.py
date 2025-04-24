import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

if __name__ == '__main__':
    df = pd.read_csv('../Train_knight.csv')
    df.loc[df['knight'] == 'Jedi', 'knight'] = 1
    df.loc[df['knight'] == 'Sith', 'knight'] = 0

    header = list(df.columns)
    for col in header:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    #variances = (df.var()/df.mean()**2) * 100

    print(df['knight'].var())

    cumulative_var = df.var().cumsum()
    print('---------------------------------------------------')
    print(cumulative_var)

    #plt.plot(range(len(cumulative_var)), cumulative_var)
    #plt.xlabel('Number of components')
    #plt.ylabel('Explained variance (%)')
    #plt.savefig('variance.png', dpi=300)