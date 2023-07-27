import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import pandas as pd
import requests

class forex_connection(ExperimentalBaseConnection):
    def __init__(self, connection_name, **kwargs):
        super().__init__(connection_name, **kwargs)

    def _connect(self):
        # This method is called when the connection is initialized.
        # For this example, we don't need any setup or initialization,
        # so we leave it empty.
        pass

    def get_data_source_df(self):
        # Return the DataFrame with the IMF data
        data = {
            'Abbreviation': ['imf', 'rba', 'boc', 'snb', 'cbr', 'nbu', 'bnro', 'boi', 'nob', 'cbn', 'ecb'],
            'Full_Name': ['International Monetary Fund', 'Reserve Bank of Australia', 'Bank of Canada', 'Swiss National Bank',
                          'Central Bank of Russia', 'National Bank of Ukraine', 'National Bank of Romania', 'Bank Of Israel',
                          'Norges Bank', 'Central Bank of Nigeria', 'European Central Bank']
        }
        return pd.DataFrame(data)
    
    @st.cache_data()
    def query(_self, base=None, symbols=None, places=None, source=None):
        base_url = 'https://api.exchangerate.host/latest'
        params = {'base': base} if base else {'base': 'USD'}

        # Add optional parameters to the request if provided
        if symbols:
            params['symbols'] = symbols
        if places:
            params['places'] = places
        if source:
            params['source'] = source

        try:
            response = requests.get(base_url, params=params)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()

                # Extract rates data from the response
                rates = data.get('rates', {})

                # Convert the rates data to a DataFrame
                df = pd.DataFrame.from_dict(rates, orient='index', columns=['Rate'])

                return df
            else:
                st.error(f"Failed to retrieve data. Status code: {response.status_code}")
                return None

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to retrieve data. Error: {e}")
            return None
