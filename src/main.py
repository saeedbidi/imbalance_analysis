import os
from bmrs_client import BMRSClient
from report_generator import ReportGenerator
from plotter import plot_imbalance, plot_hourly_imbalance

def main():
    # Set the output path
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_path, exist_ok=True)

    # Fetch data from the BMRS API for a specific settlement date
    settlement_date = "2023-10-24"
    client = BMRSClient()
    data = client.get_system_prices(settlement_date)
    
    # Generate report
    report = ReportGenerator(data)
    
    # Output and save report with weekly trend included
    print(report.generate_report_message(include_weekly_trend=True))
    report.save_report(output_path, include_weekly_trend=True)

    # Plot and save visuals to the output directory
    plot_imbalance(data, output_path)
    plot_hourly_imbalance(data, output_path)

if __name__ == "__main__":
    main()
