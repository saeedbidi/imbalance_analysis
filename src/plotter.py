import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_imbalance(data: pd.DataFrame, output_path: str):
    """
    Plot the net imbalance volume over time and save the plot as an image file.

    Args:
        data (pd.DataFrame): DataFrame containing imbalance data with a DateTime index and a 'netImbalanceVolume' column.
        output_path (str): The path where the plot image file will be saved.
    """
    plt.figure(figsize=(12, 6), dpi=300)
    data['netImbalanceVolume'].plot(
        title="Net Imbalance Volume Over Time",
        linewidth=2,  # Thicker line for clarity
        color="royalblue"  # Optional colour adjustment
    )
    
    # Enhancing font sizes for readability
    plt.title("Net Imbalance Volume Over Time", fontsize=16)
    plt.ylabel("Net Imbalance Volume (MWh)", fontsize=14)
    plt.xlabel("Time", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Saving with enhanced quality
    plot_file_path = os.path.join(output_path, "imbalance_plot.png")
    plt.savefig(plot_file_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"High-quality plot saved to {plot_file_path}")