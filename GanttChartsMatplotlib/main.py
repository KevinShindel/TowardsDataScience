import numpy as np
from pandas import DataFrame, Categorical, date_range, Series
from pandas._libs.tslibs.offsets import Day
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from string import ascii_uppercase


def main():
    MAX_LEN = 10
    TASK = [f'TASK {letter}' for letter in ascii_uppercase[:10]]
    DEP = ['IT', 'MKT', 'ENG', 'PROD', 'FIN']
    DATE_RANGE = date_range(start='2022-02-15', end='2022-03-10', freq='D', normalize=True)
    # SHIFT_PERIODS = np.random.randint(low=1, high=MAX_LEN, size=MAX_LEN)
    START = np.random.choice(DATE_RANGE, MAX_LEN)
    END = map(lambda v: np.datetime64(v) + Day(np.random.randint(low=1, high=MAX_LEN, size=1)), START)
    data = {
        # 'Task': Categorical(np.random.choice(TASK, MAX_LEN)),
        'Task': TASK,
        'Department': Categorical(np.random.choice(DEP, MAX_LEN)),
        'Start': Series(START).dt.date,
        'End': Series(END).dt.date,
        'Completion': np.round(np.random.random(MAX_LEN), 1),
    }
    df = DataFrame(data=data)

    # project start date
    proj_start = df["Start"].min()
    # number of days from project start to task start
    df['start_num'] = (df["Start"] - proj_start).dt.days
    # number of days from project start to end of tasks
    df['end_num'] = (df["End"] - proj_start).dt.days
    # days between start and end of each task
    df['days_start_to_end'] = df.end_num - df.start_num

    # basic plot
    fig, ax = plt.subplots(1, figsize=(16, 6))
    ax.barh(df["Task"], df["days_start_to_end"], left=df["start_num"])
    plt.show()

    c_dict = {'MKT': '#E64646', 'FIN': '#E69646', 'ENG': '#34D05C', 'PROD': '#34D0C3', 'IT': '#3475D0'}
    df['color'] = df['Department'].map(c_dict)

    # advanced plot
    fig, ax = plt.subplots(1, figsize=(16, 6))
    ax.barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color)
    ##### LEGENDS #####
    c_dict = {'MKT': '#E64646', 'FIN': '#E69646', 'ENG': '#34D05C',
              'PROD': '#34D0C3', 'IT': '#3475D0'}
    legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
    plt.legend(handles=legend_elements)
    ##### TICKS #####
    xticks = np.arange(0, df.end_num.max() + 1, 3)
    xticks_labels = date_range(proj_start, end=df.End.max()).strftime("%m/%d")
    xticks_minor = np.arange(0, df.end_num.max() + 1, 1)
    ax.set_xticks(xticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(xticks_labels[::3])
    plt.show()

    df['current_num'] = (df.days_start_to_end * df.Completion)


    fig, ax = plt.subplots(1, figsize=(16, 6))
    # bars
    ax.barh(df.Task, df.current_num, left=df.start_num, color=df.color)
    ax.barh(df.Task, df.days_start_to_end, left=df.start_num, color=df.color, alpha=0.5)
    # texts
    for idx, row in df.iterrows():
        ax.text(row.end_num + 0.1, idx,
                f"{int(row.Completion * 100)}%",
                va='center', alpha=0.8)
    ##### LEGENDS #####
    c_dict = {'MKT': '#E64646', 'FIN': '#E69646', 'ENG': '#34D05C', 'PROD': '#34D0C3', 'IT': '#3475D0'}
    legend_elements = [Patch(facecolor=c_dict[i], label=i) for i in c_dict]
    plt.legend(handles=legend_elements)
    ##### TICKS #####
    xticks = np.arange(0, df.end_num.max() + 1, 3)
    xticks_labels = date_range(proj_start, end=df.End.max()).strftime("%m/%d")
    xticks_minor = np.arange(0, df.end_num.max() + 1, 1)
    ax.set_xticks(xticks)
    ax.set_xticks(xticks_minor, minor=True)
    ax.set_xticklabels(xticks_labels[::3])
    plt.show()


if __name__ == '__main__':
    main()
