import pandas as pd
import matplotlib.pyplot as plt

def plot_skills():
    data = pd.read_csv('../Test_knight.csv')
    header = list(data.columns)
    fig, ax = plt.subplots(6, 5, figsize=(20, 20))
    row = 0
    col = 0
    for skill in header:
        df = pd.DataFrame(data[skill])
        df.hist(column=skill, bins=42, grid=False, color='green', alpha=0.42, ax=ax[row][col], label='Knight')
        ax[row][col].legend(['Knight'])
        if col == 4:
            col = 0
            row += 1
        else:
            col += 1
    plt.savefig('skills.jpg', dpi=300)

def plot_skill_interactions():
    data = pd.read_csv('../Train_knight.csv')
    jedi = data[data['knight'] == 'Jedi']
    sith = data[data['knight'] == 'Sith']
    header = list(data.columns)
    header.remove('knight')
    fig, ax = plt.subplots(6, 5, figsize=(20, 20))
    row = 0
    col = 0
    for skill in header:
        df = pd.DataFrame(jedi[skill])
        df.hist(column=skill, bins=42, grid=False, color='blue', alpha=0.42, ax=ax[row][col], label='Jedi')
        df = pd.DataFrame(sith[skill])
        df.hist(column=skill, bins=42, grid=False, color='red', alpha=0.42, ax=ax[row][col], label='Sith')
        ax[row][col].legend(['Jedi', 'Sith'])
        if col == 4:
            col = 0
            row += 1
        else:
            col += 1
    plt.savefig('skill_interactions.jpg', dpi=300)


if __name__ == '__main__':
    plot_skills()
    plot_skill_interactions()