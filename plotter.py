import pandas as pd
import matplotlib.pyplot as plt


def plot_imbalance(data: pd.DataFrame):
    """
    Plot the net imbalance volume over time.

    Args:
        data (pd.DataFrame): DataFrame containing imbalance data with a DateTime index and a 'netImbalanceVolume' column.
    """
    # plt.figure(figsize=(10, 5))
    # plt.plot(data.index, data['netImbalanceVolume'], label="Net Imbalance Volume", color="royalblue")
    # plt.title("Net Imbalance Volume Over Time")
    # plt.xlabel("Time")
    # plt.ylabel("Net Imbalance Volume (MWh)")
    # plt.legend()
    # plt.grid(True)
    # plt.show()
    plt.figure(figsize=(10, 5))
    data['netImbalanceVolume'].plot(title="Net Imbalance Volume Over Time")
    plt.ylabel("Net Imbalance Volume (MWh)")
    plt.xlabel("Time")
    plt.show()