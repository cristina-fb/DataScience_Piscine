import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('../Train_knight.csv')
    df.loc[df['knight'] == 'Jedi', 'knight'] = 1
    df.loc[df['knight'] == 'Sith', 'knight'] = 0
    correlation = df.corr()['knight']
    correlation = correlation.sort_values(ascending=False)
    print(correlation)