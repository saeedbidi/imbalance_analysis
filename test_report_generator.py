import pytest
import pandas as pd
from report_generator import ReportGenerator

class TestReportGenerator:

    def setup_method(self):
        """Setup sample data for testing."""
        sample_data = {
            'timestamp': pd.date_range(start="2023-10-24", periods=48, freq='30T'),
            'systemSellPrice': [50] * 48,
            'systemBuyPrice': [100] * 48,
            'netImbalanceVolume': [100, -100] * 24
        }
        df = pd.DataFrame(sample_data).set_index('timestamp')
        self.report = ReportGenerator(df)

    def test_calculate_daily_imbalance_cost(self):
        """Test daily imbalance cost calculation."""
        assert self.report.calculate_daily_imbalance_cost() == 300000