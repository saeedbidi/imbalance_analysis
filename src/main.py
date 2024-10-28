import os
import pandas as pd
from datetime import datetime
from bmrs_client import BMRSClient
from report_generator import ReportGenerator
from plotter import plot_imbalance, plot_hourly_imbalance, plot_peak_off_peak, plot_clustered_usage


def main():
    """
    Main function to process daily imbalance data for a specific date, generate a report,
    and create visualisations for further analysis.

    This function coordinates the workflow from fetching data to generating reports and visualising
    trends. It’s designed to be flexible enough to save reports, create multiple plots, and
    facilitate daily monitoring of imbalance costs.
    """
    # Set the output path for saved reports and plots
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_path, exist_ok=True)  # Ensure the output directory exists

    # Initialise BMRS client to fetch market data
    client = BMRSClient()

    # Define the date for half-hourly analysis (this can be adjusted for different dates)
    target_date = "2023-10-24"

    # Fetch data for the specified date
    try:
        data = client.get_system_prices(target_date)
    except Exception as e:
        print(f"Failed to fetch data for {target_date}: {e}")
        return

    # Set frequency to half-hourly to ensure consistent time intervals
    data.index.freq = '30T'  # Ensures data is structured in 30-minute intervals

    # Generate imbalance costs and populate the data for daily reporting
    report = ReportGenerator(data)
    report.calculate_daily_imbalance_cost()  # Adds 'imbalanceCost' column for daily analysis

    # Output and save the generated report for the day
    print(report.generate_report_message(include_weekly_trend=True))
    report.save_report(output_path, include_weekly_trend=True)

    # Plot and save various visualisations of the data
    plot_imbalance(data, output_path, window=3, annotate_peaks=True)  # Moving average with peak annotations
    plot_hourly_imbalance(data, output_path)  # Hourly breakdown of imbalance volume
    plot_peak_off_peak(data, output_path)  # Visualisation of peak and off-peak usage
    plot_clustered_usage(data, output_path)  # Clustered analysis of usage patterns

if __name__ == "__main__":
    main()
