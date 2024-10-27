import os
import pandas as pd
import numpy as np

class ReportGenerator:
    """Processes system prices and volumes data to generate daily imbalance reports."""

    def __init__(self, data: pd.DataFrame):
        """Initialise with data for processing."""
        self.data = data

    def calculate_daily_imbalance_cost(self) -> float:
        """
        Calculates the total daily imbalance cost by summing half-hourly costs.

        Returns:
            float: Total daily imbalance cost.
        """
        # Calculate imbalance cost per every half hour
        # self.data['imbalanceCost'] = self.data.apply(
        #     lambda row: abs(row['netImbalanceVolume']) * 
        #                 (row['systemSellPrice'] if row['netImbalanceVolume'] < 0 else row['systemBuyPrice']),
        #     axis=1
        # )

        # Vectorised: Calculate imbalance cost per half hour with a fully vectorised way using Numpy
        imbalance_costs = np.where(
            self.data['netImbalanceVolume'] < 0,
            abs(self.data['netImbalanceVolume']) * self.data['systemSellPrice'],
            abs(self.data['netImbalanceVolume']) * self.data['systemBuyPrice']
        )
        self.data['imbalanceCost'] = imbalance_costs
        total_cost = self.data['imbalanceCost'].sum()
        return total_cost

    def calculate_unit_rate(self) -> float:
        """
        Calculates the unit rate of imbalance cost per MWh.

        Returns:
            float: Daily imbalance unit rate.
        """
        total_volume = self.data['netImbalanceVolume'].abs().sum()
        total_cost = self.calculate_daily_imbalance_cost()
        return total_cost / total_volume if total_volume > 0 else 0 # Avoid division by zero in case of zero total volume

    def hour_with_highest_imbalance(self) -> int:
        """
        Identifies the hour with the highest absolute imbalance volume.

        Returns:
            int: Hour of the day with the highest imbalance volume.

        """
        self.data['hour'] = self.data.index.hour
        hourly_imbalance = self.data.groupby('hour')['netImbalanceVolume'].sum().abs()
        peak_hour = hourly_imbalance.idxmax()
        return peak_hour
    
    def calculate_daily_average_imbalance(self) -> float:
        """
        Calculate the daily average net imbalance volume.

        Args:
            data (pd.DataFrame): DataFrame containing imbalance data with a 'netImbalanceVolume' column.

        Returns:
            float: The daily average net imbalance volume.
        """
        daily_average = self.data['netImbalanceVolume'].mean()
        return round(daily_average, 2)

    def generate_report_message(self) -> str:
        """
        Generate a summary message with the imbalance cost, unit rate, and peak imbalance hour.

        Returns:
            str: Formatted report message.
        """
        total_cost = self.calculate_daily_imbalance_cost()
        unit_rate = self.calculate_unit_rate()
        peak_hour = self.hour_with_highest_imbalance()
        daily_average = self.calculate_daily_average_imbalance()
        
        return (f"Total Daily Imbalance Cost: £{total_cost:.2f}\n"
                f"Daily Imbalance Unit Rate: £{unit_rate:.2f}/MWh\n"
                f"Hour with Highest Imbalance Volume: {peak_hour}:00\n\n\n"
                f"Extra analysis:\n"
                f"Daily Average Net Imbalance Volume: {daily_average} MWh")
    
    def save_report(self, output_path: str) -> None:
        """
        Save the generated report message to a text file in the specified output path.

        Args:
            output_path (str): The path where the report text file will be saved.
        """
        report_message = self.generate_report_message()
        report_file_path = os.path.join(output_path, "daily_imbalance_report.txt")
        with open(report_file_path, "w") as file:
            file.write(report_message)
        print(f"Report saved to {report_file_path}")