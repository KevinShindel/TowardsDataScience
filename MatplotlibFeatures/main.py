import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = pd.read_csv("sales_vs_discount.csv")
    df["date"] = df["date"].astype("datetime64[ns]")
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["sales_amount"])
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["sales_amount"])
    plt.plot(df["date"], df["discount"])
    plt.show()

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    ax1.plot(df["date"], df["sales_amount"])
    ax2.plot(df["date"], df["discount"], color="r")
    ax1.set_ylabel("sales amount", fontsize=18)
    ax1.set_ylim([0, 6000])
    ax2.set_ylabel("discount rate", fontsize=18)
    ax2.set_ylim([0, 1])
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["sales_amount"])
    plt.xticks(fontsize=14, rotation=45)
    plt.yticks(ticks=np.arange(0, 6000, 500), fontsize=14)
    plt.ylabel("Sales Amount", fontsize=18)
    plt.show()

    fig, (ax1, ax2) = plt.subplots(
        nrows=2, ncols=1, sharex=True, figsize=(12, 6)
    )
    fig.tight_layout(pad=2)
    ax1.plot(df["date"], df["sales_amount"])
    ax2.plot(df["date"], df["discount"])
    ax1.set_ylabel("Sales", fontsize=18)
    ax2.set_ylabel("Discount", fontsize=18)
    plt.show()

    fig, axs = plt.subplots(
        nrows=2, ncols=1, sharex=True, figsize=(12, 6)
    )
    fig.tight_layout(pad=2)
    axs[0].plot(df["date"], df["sales_amount"])
    axs[1].plot(df["date"], df["discount"])
    axs[0].set_ylabel("Sales", fontsize=18)
    axs[1].set_ylabel("Discount", fontsize=18)
    plt.show()


if __name__ == '__main__':
    main()
