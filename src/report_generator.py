import os
import pandas as pd
import numpy as np

class ReportGenerator:
    """Processes system prices and volume data to generate detailed daily imbalance reports."""

    def __init__(self, data: pd.DataFrame):
        """Initialise the report generator with imbalance data, ready for processing."""
        self.data = data

    def calculate_daily_imbalance_cost(self) -> float:
        """
        Calculate the total daily imbalance cost based on whether the system was in a net sell or buy position.
        
        If the imbalance volume is negative, it implies a net sell, and the cost is calculated using the sell price.
        Otherwise, the buy price is used. This provides a comprehensive daily cost that reflects the true 
        market impact of imbalances.
        
        Returns:
            float: Total daily imbalance cost.
        """
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
        Calculate the average unit cost per MWh of imbalance, taking into account total volume and cost.
        
        This provides insight into the cost efficiency of imbalances on a per-unit basis, 
        allowing for easy comparison with other days or operational targets.
        
        Returns:
            float: Daily imbalance unit rate (£/MWh).
        """
        total_volume = self.data['netImbalanceVolume'].abs().sum()
        total_cost = self.calculate_daily_imbalance_cost()
        return total_cost / total_volume if total_volume > 0 else 0

    def hour_with_highest_imbalance(self) -> int:
        """
        Identify the hour of the day with the highest net imbalance, indicating peak volatility.

        This could highlight operational patterns or specific times of day when the system 
        experiences significant shifts, which might be worth investigating further.
        
        Returns:
            int: The hour (0-23) when the imbalance volume peaks.
        """
        self.data['hour'] = self.data.index.hour
        hourly_imbalance = self.data.groupby('hour')['netImbalanceVolume'].sum().abs()
        peak_hour = hourly_imbalance.idxmax()
        return peak_hour
    
    def calculate_daily_average_imbalance(self) -> float:
        """
        Compute the average imbalance volume over the course of the day.
        
        This gives a quick sense of the day’s average net imbalance, offering a benchmark 
        for comparing daily fluctuations or identifying unusually high or low imbalance days.
        
        Returns:
            float: The daily average net imbalance volume, rounded to two decimal places.
        """
        daily_average = self.data['netImbalanceVolume'].mean()
        return round(daily_average, 2)
    
    def calculate_hourly_imbalance_cost(self) -> pd.Series:
        """
        Calculate the imbalance cost for each hour, providing a detailed breakdown of costs by time of day.
        
        This allows for analysis of hourly fluctuations in imbalance costs, which may reveal patterns 
        or peak periods that align with system demand or market events.
        
        Returns:
            pd.Series: Total hourly imbalance cost, indexed by hour.
        """
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
        Calculate and return the weekly trend of daily imbalance costs.
        
        This gives a broader view, allowing for trend analysis over multiple days, helping 
        to spot any recurring weekly patterns in the data or unusual spikes in costs.
        
        Returns:
            pd.Series: Weekly imbalance cost trend, indexed by week.
        """
        self.data['date'] = pd.to_datetime(self.data.index.date)
        daily_cost = self.data.groupby('date')['imbalanceCost'].sum()
        daily_cost.index = pd.to_datetime(daily_cost.index)
        weekly_trend = daily_cost.resample('W').sum()
        
        return weekly_trend

    def generate_report_message(self, include_weekly_trend=False) -> str:
        """
        Generate a comprehensive summary report of the daily imbalance data.
        
        The report includes total cost, unit rate, peak hour, daily average, and optionally, 
        the weekly trend. This summary provides an easily readable output for daily review 
        or broader insights when the weekly trend is included.
        
        Args:
            include_weekly_trend (bool): Whether to include the weekly trend in the report.
        
        Returns:
            str: The formatted report message.
        """
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
        Save the generated report message to a text file, optionally including the weekly trend.
        
        This method provides a persistent record of the daily report, saved to a text file, 
        which can be referred back to for auditing, analysis, or trend tracking.
        
        Args:
            output_path (str): The directory where the report file should be saved.
            include_weekly_trend (bool): Whether to include the weekly trend in the saved report.
        """
        report_message = self.generate_report_message(include_weekly_trend=include_weekly_trend)
        report_file_path = os.path.join(output_path, "daily_imbalance_report.txt")
        with open(report_file_path, "w") as file:
            file.write(report_message)
        print(f"Report saved to {report_file_path}")
