import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    df_test = pd.read_csv('../Test_knight.csv')
    df_train = pd.read_csv('../Train_knight.csv')
    jedi = df_train[df_train['knight'] == 'Jedi']
    sith = df_train[df_train['knight'] == 'Sith']
    
    fig, ax = plt.subplots(2,2, figsize=(10, 10))
    
    jedi.plot.scatter('Empowered','Stims',ax=ax[0][0], alpha=0.42, color='blue', label='Jedi')
    sith.plot.scatter('Empowered','Stims',ax=ax[0][0], alpha=0.42, color='red', label='Sith')
    df_test.plot.scatter('Empowered','Stims',ax=ax[1][0], alpha=0.42, color='green', label='knight')

    jedi.plot.scatter('Push','Deflection',ax=ax[0][1], alpha=0.42, color='blue', label='Jedi')
    sith.plot.scatter('Push','Deflection',ax=ax[0][1], alpha=0.42, color='red', label='Sith')
    df_test.plot.scatter('Push','Deflection',ax=ax[1][1], alpha=0.42, color='green', label='knight')
    # plt.show()
    plt.savefig('scatter.jpg')