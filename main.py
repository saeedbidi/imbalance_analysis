from bmrs_client import BMRSClient
from report_generator import ReportGenerator
from plotter import plot_imbalance

def main():
    # Fetch data from the BMRS API for a specific settlement date
    settlement_date = "2023-10-24"
    client = BMRSClient()
    data = client.get_system_prices(settlement_date)
    
    # Generate report
    report = ReportGenerator(data)
    
    # Output
    print(report.generate_report_message())
    
    # Plot
    plot_imbalance(data)

if __name__ == "__main__":
    main()
