import os
import pandas as pd
import numpy as np

class ReportGenerator:
    """Processes system prices and volumes data to generate daily imbalance reports."""

    def __init__(self, data: pd.DataFrame):
        """Initialise with data for processing."""
        self.data = data

    def calculate_daily_imbalance_cost(self) -> float:
        imbalance_costs = np.where(
            self.data['netImbalanceVolume'] < 0,
            abs(self.data['netImbalanceVolume']) * self.data['systemSellPrice'],
            abs(self.data['netImbalanceVolume']) * self.data['systemBuyPrice']
        )
        self.data['imbalanceCost'] = imbalance_costs
        total_cost = self.data['imbalanceCost'].sum()
        return total_cost

    def calculate_unit_rate(self) -> float:
        total_volume = self.data['netImbalanceVolume'].abs().sum()
        total_cost = self.calculate_daily_imbalance_cost()
        return total_cost / total_volume if total_volume > 0 else 0

    def hour_with_highest_imbalance(self) -> int:
        self.data['hour'] = self.data.index.hour
        hourly_imbalance = self.data.groupby('hour')['netImbalanceVolume'].sum().abs()
        peak_hour = hourly_imbalance.idxmax()
        return peak_hour
    
    def calculate_daily_average_imbalance(self) -> float:
        daily_average = self.data['netImbalanceVolume'].mean()
        return round(daily_average, 2)
    
    def calculate_hourly_imbalance_cost(self) -> pd.Series:
        self.data['hour'] = self.data.index.hour
        self.data['hourlyImbalanceCost'] = np.where(
            self.data['netImbalanceVolume'] < 0,
            abs(self.data['netImbalanceVolume']) * self.data['systemSellPrice'],
            abs(self.data['netImbalanceVolume']) * self.data['systemBuyPrice']
        )
        hourly_cost = self.data.groupby('hour')['hourlyImbalanceCost'].sum()
        return hourly_cost

    def calculate_weekly_trend(self) -> pd.Series:
        """
        Calculate the weekly trend of total daily imbalance cost.
        """
        self.data['date'] = pd.to_datetime(self.data.index.date)
        daily_cost = self.data.groupby('date')['imbalanceCost'].sum()
        daily_cost.index = pd.to_datetime(daily_cost.index)
        weekly_trend = daily_cost.resample('W').sum()
        
        return weekly_trend

    def generate_report_message(self, include_weekly_trend=False) -> str:
        total_cost = self.calculate_daily_imbalance_cost()
        unit_rate = self.calculate_unit_rate()
        peak_hour = self.hour_with_highest_imbalance()
        daily_average = self.calculate_daily_average_imbalance()
        hourly_cost = self.calculate_hourly_imbalance_cost()
        peak_hourly_cost = hourly_cost.max()

        report_message = (f"Total Daily Imbalance Cost: £{total_cost:.2f}\n"
                          f"Daily Imbalance Unit Rate: £{unit_rate:.2f}/MWh\n"
                          f"Hour with Highest Imbalance Volume: {peak_hour}:00\n\n\n"
                          f"Extra analysis:\n"
                          f"Daily Average Net Imbalance Volume: {daily_average:.2f} MWh\n"
                          f"Peak Hourly Imbalance Cost: £{peak_hourly_cost:.2f} at hour {hourly_cost.idxmax()}\n")
        
        if include_weekly_trend:
            weekly_trend = self.calculate_weekly_trend()
            report_message += "\nWeekly Imbalance Cost Trend:\n"
            report_message += weekly_trend.to_string()

        return report_message
    
    def save_report(self, output_path: str, include_weekly_trend=False) -> None:
        """
        Save the generated report message, with an optional weekly trend, to a text file.
        """
        report_message = self.generate_report_message(include_weekly_trend=include_weekly_trend)
        report_file_path = os.path.join(output_path, "daily_imbalance_report.txt")
        with open(report_file_path, "w") as file:
            file.write(report_message)
        print(f"Report saved to {report_file_path}")
