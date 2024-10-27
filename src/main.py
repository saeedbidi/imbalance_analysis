import os
from bmrs_client import BMRSClient
from report_generator import ReportGenerator
from plotter import plot_imbalance

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
    
    # Output
    print(report.generate_report_message())

    # Save report and plot to the output directory
    report.save_report(output_path)
    plot_imbalance(data, output_path)

if __name__ == "__main__":
    main()
