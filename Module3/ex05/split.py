import pandas as pd
from sklearn.model_selection import train_test_split


if __name__ == '__main__':
    df_train = pd.read_csv('../Train_knight.csv')
    X = df_train.drop('knight', axis='columns')
    y = df_train['knight']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.143, random_state=42, stratify=y) #14.3% of 70% training (10% of total)

    training = pd.concat([X_train, y_train], axis=1)
    validation = pd.concat([X_test, y_test], axis=1)

    training.to_csv('Training_knight.csv', index=False)
    validation.to_csv('Validation_knight.csv', index=False)