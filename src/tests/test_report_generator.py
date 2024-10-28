import pytest
import pandas as pd
import numpy as np
from src.report_generator import ReportGenerator


class TestReportGenerator:
    """
    Unit tests for the ReportGenerator class, ensuring accurate calculations for 
    daily imbalance cost, unit rate, and peak imbalance hour.
    """

    def setup_method(self):
        """Setup sample data for testing."""
        sample_data = {
            'timestamp': pd.date_range(start="2023-10-24", periods=48, freq='30min'),
            'systemSellPrice': [60] * 48,
            'systemBuyPrice': [65] * 48,
            'netImbalanceVolume': [100, -100] * 24
        }
        df = pd.DataFrame(sample_data).set_index('timestamp')
        self.report = ReportGenerator(df)

    def test_calculate_daily_imbalance_cost(self):
        """Test daily imbalance cost calculation."""
        assert self.report.calculate_daily_imbalance_cost() == 300000

    def test_calculate_unit_rate(self):
        """Test unit rate calculation."""
        assert self.report.calculate_unit_rate() == pytest.approx(62.5, rel=1e-2)

    def test_hour_with_highest_imbalance(self):
        """Test for the hour with the highest imbalance."""
        assert self.report.hour_with_highest_imbalance() == 0

    def test_calculate_daily_average_imbalance(self):
        """Test calculation of the daily average imbalance volume."""
        assert self.report.calculate_daily_average_imbalance() == 0  # Since imbalance alternates between 100 and -100

    def test_calculate_hourly_imbalance_cost(self):
        """Test calculation of hourly imbalance costs."""
        hourly_cost = self.report.calculate_hourly_imbalance_cost()
        assert hourly_cost[0] == 12500  # Expected value based on alternating volumes and buy/sell prices

    def test_calculate_weekly_trend(self):
        """Test weekly trend calculation for imbalance costs."""
        weekly_trend = self.report.calculate_weekly_trend()
        assert len(weekly_trend) == 1  # Expecting a single week for a single day of data
        assert weekly_trend.iloc[0] == 300000  # Total imbalance cost for the period

    def test_data_integrity(self):
        """Ensure data structure integrity."""
        assert 'imbalanceCost' not in self.report.data.columns  # Before calculation, this column should not exist
        self.report.calculate_daily_imbalance_cost()
        assert 'imbalanceCost' in self.report.data.columns  # After calculation, it should exist
        assert self.report.data['imbalanceCost'].dtype == 'float64'

    def test_zero_imbalance_volume(self):
        """Test handling of zero net imbalance volume."""
        self.report.data['netImbalanceVolume'] = 0
        assert self.report.calculate_daily_imbalance_cost() == 0
        assert self.report.calculate_unit_rate() == 0

    def test_all_positive_imbalance_volume(self):
        """Test with all positive net imbalance volumes."""
        self.report.data['netImbalanceVolume'] = 100  # All positive values
        assert self.report.calculate_daily_imbalance_cost() == 312000  # Expected value with all positive

    def test_all_negative_imbalance_volume(self):
        """Test with all negative net imbalance volumes."""
        self.report.data['netImbalanceVolume'] = -100  # All negative values
        assert self.report.calculate_daily_imbalance_cost() == 288000  # Expected value with all negative

    def test_missing_column(self):
        """Test behaviour with missing columns."""
        self.report.data.drop(columns=['systemSellPrice'], inplace=True)
        with pytest.raises(KeyError):
            self.report.calculate_daily_imbalance_cost()

    def test_generate_report_message(self):
        """Test report message generation with key metrics included."""
        message = self.report.generate_report_message()
        assert "Total Daily Imbalance Cost" in message
        assert "Daily Imbalance Unit Rate" in message
        assert "Hour with Highest Imbalance Volume" in message

    def test_save_report(self, tmp_path):
        """Test saving the report file."""
        output_path = tmp_path / "output"
        output_path.mkdir()
        self.report.save_report(str(output_path))
        
        # Check if the report file exists and contains expected content
        report_file = output_path / "daily_imbalance_report.txt"
        assert report_file.exists()
        
        with open(report_file, "r") as f:
            content = f.read()
        assert "Total Daily Imbalance Cost" in content
