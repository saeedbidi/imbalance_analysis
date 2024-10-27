import pytest
import pandas as pd
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
        # print('df=',df)
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