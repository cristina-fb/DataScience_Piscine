import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor


if __name__ == '__main__':
    df = pd.read_csv('../Train_knight.csv')
    df.loc[df['knight'] == 'Jedi', 'knight'] = 1
    df.loc[df['knight'] == 'Sith', 'knight'] = 0
    df['knight'] = df['knight'].astype(int)
    header = list(df.columns)
    for col in header:
        df[col] = (df[col] - df[col].mean()) / df[col].std()
    vif_data = pd.DataFrame()
    vif_data["Feature"] = df.columns
    vif_data["VIF"] = [variance_inflation_factor(df.values, i) for i in range(len(df.columns))]
    vif_data["Tolerance"] = [1/vif_data.loc[i, 'VIF'] for i in range(len(df.columns))]
    vif_data = vif_data.sort_values(by=['VIF'], ascending=False)
    vif_data.reset_index(drop=True, inplace=True)
    print(vif_data)
    print('---------------------------------------------------')
    vif = vif_data.loc[vif_data['VIF'] <= 5]
    print(vif)