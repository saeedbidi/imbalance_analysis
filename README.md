
# SE BMRS Reporting

## Author
Developed by Saeed Bidi, PhD

## Overview

This project provides a tool for analysing daily electricity system imbalance costs and prices using BMRS (Balancing Mechanism Reporting Service) data. The aim is to collect, process, and analyse imbalance data to provide insights into daily electricity market behaviour. The output includes a report summarising key metrics, detailed data visualisations, and a robust testing suite to ensure accuracy and maintainability.

The analysis can help identify patterns in electricity system imbalances, such as high or low usage periods, average imbalance volumes, and unit rates. Additionally, the code is designed to be easily extendable and adaptable for future needs, such as incorporating advanced modelling or predictive algorithms.

## Features

- **Data Retrieval**: Fetches system prices and imbalance volumes from BMRS's API.
- **Data Analysis and Reporting**: Computes daily imbalance costs, peak imbalance hours, and average unit rates.
- **Visualisation**: Generates several insightful plots, including hourly imbalance volume, peak and off-peak periods, and cluster-based analysis of usage.
- **Testing Suite**: Provides comprehensive tests for all core calculations and processes to ensure data integrity and code reliability.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/se_bmrs_reporting.git
   cd se_bmrs_reporting
   ```

2. **Set up a virtual environment and activate it:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows, use 'myenv\Scripts\activate'
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests:**
   To ensure everything is set up correctly and all modules work as expected, run:
   ```bash
   pytest
   ```

## Usage Guide

1. **Fetching and Processing Data:**
   The `main.py` file is the main entry point to fetch data, process it, and generate reports. You can adjust the target date for analysis within this file. 

   ```python
   # Inside main.py, update the target_date as needed
   target_date = "2023-10-24"  # Example date for analysis
   ```

2. **Generating Daily Reports and Plots:**
   Running `main.py` will produce:
   - A detailed daily imbalance report saved to `output/daily_imbalance_report.txt`
   - Several plots visualising the imbalance data saved in the `output` directory.

   ```bash
   python main.py
   ```

3. **Output Summary:**
   - **Report**: Provides key metrics such as total daily imbalance cost, unit rate, peak imbalance hour, and daily averages.
   - **Plots**:
     - `hourly_imbalance_volume.png`: Shows the hourly breakdown of imbalance volume.
     - `imbalance_plot_with_moving_average.png`: A line plot of imbalance volume over time, with a smoothed moving average.
     - `peak_off_peak_plot.png`: Highlights peak and off-peak usage periods.
     - `clustered_usage_plot.png`: Groups imbalance volumes by clusters to visualise usage levels (e.g., low, medium, high).

## Project Structure

```
SE_BMRS_REPORTING
├── src
│   ├── bmrs_client.py              # BMRS API client to fetch imbalance data
│   ├── main.py                     # Main file to execute data processing and visualisation
│   ├── plotter.py                  # Contains all visualisation functions
│   └── report_generator.py         # Calculates and generates the daily imbalance report
├── tests
│   └── test_report_generator.py    # Unit tests for report generation
├── output                          # Output directory for reports and plots
│   └── *.png, *.txt                # Generated report and plots
├── requirements.txt                # List of dependencies
├── README.md                       # Project documentation
└── setup.py                        # Setup file for packaging (if required)
```

## Approach

1. **Data Collection**: The `BMRSClient` class in `bmrs_client.py` handles data retrieval from the BMRS API. The data is collected for a specified date and includes system buy and sell prices as well as the net imbalance volume.

2. **Data Processing and Report Generation**: The `ReportGenerator` class processes the data to compute:
   - **Total Daily Imbalance Cost**: Based on system buy and sell prices.
   - **Daily Unit Rate**: Average cost per MWh.
   - **Peak Imbalance Hour**: The hour with the highest imbalance volume.
   - **Daily Averages**: Provides a quick overview of the day's imbalance volume.

3. **Visualisation**: The `plotter.py` module contains multiple functions to generate plots that help analyse the imbalance trends over time.

4. **Testing**: `test_report_generator.py` provides unit tests to ensure accurate calculations and reliable functionality across the codebase.

## Insights from Analysis

- **Hourly Imbalance Analysis**: The bar chart of hourly imbalance volume helps identify specific times when system demand is highest, indicating potential stress periods.
- **Peak and Off-Peak Thresholds**: By plotting peak and off-peak periods, we can see the periods when the system is more stable versus when it faces high demand or imbalances.
- **Cluster Analysis**: Clustering the data into low, medium, and high usage levels offers a segmented view of daily imbalance behaviour, making it easier to spot recurring patterns or anomalies.

## Future Development

Here are some potential enhancements for the project:

1. **Advanced Machine Learning Models**: 
   - Implement predictive models, such as **LSTM (Long Short-Term Memory)** networks, for time series forecasting of imbalance volumes.
   - Use models like **Random Forest** to predict peak imbalance hours based on historical data.

2. **Enhanced Visualisations**: 
   - Add more insightful visualisations, such as heatmaps, to observe day-over-day variations in imbalance costs.
   - Compare different days or weeks to see how system imbalances evolve over time.

3. **Error Handling and Robustness**: Improve error handling in the API client to account for potential issues with BMRS data availability.

## **License**
This project is open-source and available under the [MIT License](LICENSE).


