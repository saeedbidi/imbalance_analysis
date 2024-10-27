from datetime import datetime
import requests
import pandas as pd


class BMRSClient:
    """Client to interact with the BMRS API for imbalance prices and volumes."""

    def __init__(self):
        """Initialises the client with the base URL for BMRS API."""
        self.base_url = "https://data.elexon.co.uk/bmrs/api/v1" # as mentioned on the documentation

    def get_system_prices(self, settlement_date: str) -> pd.DataFrame:
        """
        Fetches system buy and sell prices along with net imbalance volume for the given date.

        Args:
            settlement_date (str): The date in 'YYYY-MM-DD' format for which to retrieve data.

        Returns:
            pd DataFrame: pandas DataFrame with columns 'timestamp', 'systemSellPrice', 'systemBuyPrice', and 'netImbalanceVolume'.
        """
        url = f"{self.base_url}/balancing/settlement/system-prices/{settlement_date}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Transform JSON data to a pandas dataframe
        records = [
            {
                "timestamp": datetime.strptime(record['startTime'], "%Y-%m-%dT%H:%M:%SZ"),
                "systemSellPrice": float(record['systemSellPrice']),
                "systemBuyPrice": float(record['systemBuyPrice']),
                "netImbalanceVolume": float(record['netImbalanceVolume'])
            }
            for record in data['data']
        ]

        df = pd.DataFrame(records)
        df.set_index("timestamp", inplace=True)
        return df