from datetime import datetime
import requests
import pandas as pd


class BMRSClient:
    """
    A simple client to interact with the BMRS API, specifically designed to retrieve system prices 
    and imbalance volume data for electricity settlements.
    """

    def __init__(self):
        """
        Sets up the BMRS API client with the base URL for accessing the API endpoints.
        
        This initialisation makes it easy to reuse the client for different requests.
        """
        self.base_url = "https://data.elexon.co.uk/bmrs/api/v1"  # API base URL as specified in the documentation

    def get_system_prices(self, settlement_date: str) -> pd.DataFrame:
        """
        Retrieves system buy and sell prices along with net imbalance volume for a specified date.
        
        This method fetches the prices and volumes data for a given settlement date and organises it
        in a structured pandas DataFrame. Ideal for analysing daily trends in electricity pricing and 
        imbalance volume.

        Args:
            settlement_date (str): Date for which to fetch the data, in 'YYYY-MM-DD' format.

        Returns:
            pd.DataFrame: A DataFrame indexed by timestamp, with columns for 'systemSellPrice', 'systemBuyPrice', 
            and 'netImbalanceVolume', providing an organised view of the fetched data.
        """
        url = f"{self.base_url}/balancing/settlement/system-prices/{settlement_date}"
        response = requests.get(url)
        response.raise_for_status()  # Ensure we raise an error if the request fails
        data = response.json()

        # Extract and transform JSON data into a DataFrame
        records = [
            {
                "timestamp": datetime.strptime(record['startTime'], "%Y-%m-%dT%H:%M:%SZ"),
                "systemSellPrice": float(record['systemSellPrice']),
                "systemBuyPrice": float(record['systemBuyPrice']),
                "netImbalanceVolume": float(record['netImbalanceVolume'])
            }
            for record in data['data']
        ]

        # Organise data into a pandas DataFrame
        df = pd.DataFrame(records)
        df.set_index("timestamp", inplace=True)
        return df
