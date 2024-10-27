import matplotlib.pyplot as plt


def plot_imbalance(self):
    """Plot the net imbalance volume over time."""
    plt.figure(figsize=(10, 5))
    self.data['netImbalanceVolume'].plot(title="Net Imbalance Volume Over Time")
    plt.ylabel("Net Imbalance Volume (MWh)")
    plt.xlabel("Time")
    plt.show()