import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    df_test = pd.read_csv('../Test_knight.csv')
    df_train = pd.read_csv('../Train_knight.csv')

    header = list(df_test.columns)
    for col in header:
        df_test[col] = (df_test[col] - df_test[col].mean()) / df_test[col].std()

    header = list(df_train.columns)
    header.remove('knight')
    for col in header:
        df_train[col] = (df_train[col] - df_train[col].mean()) / df_train[col].std()

    print(df_test)
    print('---------------------------------------------------')
    print(df_train)


    jedi = df_train[df_train['knight'] == 'Jedi'].drop('knight', axis='columns')
    sith = df_train[df_train['knight'] == 'Sith'].drop('knight', axis='columns')

    fig, ax = plt.subplots(1,2, figsize=(10, 5))
    jedi.plot.scatter('Empowered','Stims',ax=ax[0], alpha=0.42, color='blue', label='Jedi')
    sith.plot.scatter('Empowered','Stims',ax=ax[0], alpha=0.42, color='red', label='Sith')
    df_test.plot.scatter('Empowered','Stims',ax=ax[1], alpha=0.42, color='green', label='knight')
    plt.savefig('standarized.jpg', dpi=300)