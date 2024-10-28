import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def plot_imbalance(data: pd.DataFrame, output_path: str, window: int = 3, annotate_peaks: bool = True):
    """
    Create a plot of net imbalance volume over time, adding a moving average line and optional peak annotations.
    
    This plot helps to visualise the imbalance volume trends over the day with a smoother line overlay. 
    It also optionally highlights peaks and troughs for easy identification.

    Args:
        data (pd.DataFrame): DataFrame with imbalance data, indexed by DateTime, containing a 'netImbalanceVolume' column.
        output_path (str): Location to save the plot image.
        window (int): The size of the moving average window to smooth the data. Default is 3.
        annotate_peaks (bool): Whether to highlight the highest and lowest points on the plot. Default is True.
    """
    # Compute the moving average to smooth out fluctuations
    data['smoothed_imbalance'] = data['netImbalanceVolume'].rolling(window=window, center=True).mean()

    # Create the plot with both original and smoothed lines
    plt.figure(figsize=(12, 6), dpi=300)
    plt.plot(data.index, data['netImbalanceVolume'], label='Original', linewidth=2, color="blue", alpha=1)
    plt.plot(data.index, data['smoothed_imbalance'], label=f'{window}-Point Moving Average', linewidth=2, color='orange')

    # Add titles, labels, and gridlines
    plt.title("Net Imbalance Volume Over Time", fontsize=16)
    plt.ylabel("Net Imbalance Volume (MWh)", fontsize=14)
    plt.xlabel("Time", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Optionally, highlight peaks and troughs
    if annotate_peaks:
        max_value = data['netImbalanceVolume'].max()
        min_value = data['netImbalanceVolume'].min()
        plt.annotate(f'Peak: {max_value:.0f} MWh', xy=(data['netImbalanceVolume'].idxmax(), max_value), xytext=(data['netImbalanceVolume'].idxmax() + pd.Timedelta(minutes=-180), max_value - 50), ha='center', arrowprops=dict(facecolor='red', arrowstyle="->", lw=0.8), fontsize=10, color='red')
        plt.annotate(f'Trough: {min_value:.0f} MWh', xy=(data['netImbalanceVolume'].idxmin(), min_value), xytext=(data['netImbalanceVolume'].idxmin() + pd.Timedelta(minutes=180), min_value + 50), ha='center', arrowprops=dict(facecolor='green', arrowstyle="->", lw=0.8), fontsize=10, color='green')

    # Save the final plot
    plot_file_path = os.path.join(output_path, "imbalance_plot_with_moving_average.png")
    plt.savefig(plot_file_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Imbalance plot with moving average and annotations saved to {plot_file_path}")

def plot_hourly_imbalance(data: pd.DataFrame, output_path: str):
    """
    Generate a bar chart of hourly net imbalance volumes.
    
    This plot breaks down the total imbalance volume for each hour, showing the net imbalance across the day 
    and highlighting any significant peaks or troughs in volume.

    Args:
        data (pd.DataFrame): DataFrame with a 'netImbalanceVolume' column.
        output_path (str): The path where the plot image file will be saved.
    """
    data['hour'] = data.index.hour
    hourly_volume = data.groupby('hour')['netImbalanceVolume'].sum()

    # Plot the data in bar chart form
    plt.figure(figsize=(12, 6), dpi=300)
    ax = hourly_volume.plot(kind='bar', color='teal')
    plt.title("Hourly Imbalance Volume", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Net Imbalance Volume (MWh)", fontsize=14)
    plt.xticks(fontsize=12, rotation=45, ha='right')
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Save the hourly plot
    plot_path = os.path.join(output_path, "hourly_imbalance_volume.png")
    plt.savefig(plot_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Hourly imbalance volume plot saved at {plot_path}")

def plot_peak_off_peak(data: pd.DataFrame, output_path: str):
    """
    Create a plot of net imbalance volume with peak and off-peak periods highlighted.
    
    This plot helps distinguish between high-demand (peak) and low-demand (off-peak) periods, 
    defined by the top and bottom 25% quantiles of the data.

    Args:
        data (pd.DataFrame): DataFrame with imbalance data, including 'netImbalanceVolume' and a DateTime index.
        output_path (str): Directory to save the plot image.
    """
    peak_threshold = data['netImbalanceVolume'].quantile(0.75)
    off_peak_threshold = data['netImbalanceVolume'].quantile(0.25)

    # Label peak and off-peak periods
    data['usage_period'] = data['netImbalanceVolume'].apply(lambda x: 'Peak' if x >= peak_threshold else ('Off-Peak' if x <= off_peak_threshold else 'Normal'))

    # Plot with peak and off-peak thresholds
    plt.figure(figsize=(12, 6), dpi=300)
    plt.plot(data.index, data['netImbalanceVolume'], label="Net Imbalance Volume", linewidth=2, color="blue")
    plt.axhline(peak_threshold, color="red", linestyle="--", linewidth=1.5, label="Peak Threshold (Top 25%)")
    plt.axhline(off_peak_threshold, color="green", linestyle="--", linewidth=1.5, label="Off-Peak Threshold (Bottom 25%)")
    plt.title("Net Imbalance Volume with Peak and Off-Peak Thresholds", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Net Imbalance Volume (MWh)", fontsize=14)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Save the plot
    plot_file_path = os.path.join(output_path, "peak_off_peak_plot.png")
    plt.savefig(plot_file_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Peak and off-peak plot saved to {plot_file_path}")

def plot_clustered_usage(data: pd.DataFrame, output_path: str, n_clusters: int = 3):
    """
    Perform clustering on net imbalance volume to highlight usage levels.
    
    This function uses K-means clustering to categorise data points into groups, such as low, medium, 
    and high usage, and displays each cluster with a different colour for easy visual analysis.

    Args:
        data (pd.DataFrame): DataFrame with imbalance data, including a 'netImbalanceVolume' column and DateTime index.
        output_path (str): Directory to save the clustered usage plot.
        n_clusters (int): Number of clusters to create. Default is 3 (typically low, medium, and high usage).
    """
    # Reshape data for clustering
    usage_data = data[['netImbalanceVolume']].copy()
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(usage_data)
    usage_data['cluster'] = kmeans.labels_

    # Map clusters to descriptive labels (e.g., 'Low Usage', 'Medium Usage', 'High Usage')
    cluster_means = usage_data.groupby('cluster')['netImbalanceVolume'].mean()
    sorted_clusters = cluster_means.sort_values().index
    cluster_names = {sorted_clusters[0]: 'Low Usage', sorted_clusters[1]: 'Medium Usage', sorted_clusters[2]: 'High Usage'}
    usage_data['usage_label'] = usage_data['cluster'].map(cluster_names)

    # Plot with custom colours for each usage label
    plt.figure(figsize=(12, 6), dpi=300)
    colors = {'Low Usage': 'green', 'Medium Usage': 'orange', 'High Usage': 'red'}
    for label, cluster_data in usage_data.groupby('usage_label'):
        plt.scatter(cluster_data.index, cluster_data['netImbalanceVolume'], label=label, color=colors[label])

    plt.title("Clustered Electricity Usage", fontsize=16)
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Net Imbalance Volume (MWh)", fontsize=14)
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)

    # Save clustered plot
    plot_file_path = os.path.join(output_path, "clustered_usage_plot.png")
    plt.savefig(plot_file_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Clustered usage plot saved to {plot_file_path}")