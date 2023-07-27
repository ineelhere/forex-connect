import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
import pandas as pd
import requests

class ForexConnection(ExperimentalBaseConnection):
    def __init__(self, connection_name, **kwargs):
        super().__init__(connection_name, **kwargs)

    def _connect(self):
        # This method is called when the connection is initialized.
        # For this example, we don't need any setup or initialization,
        # so we leave it empty.
        pass

    def query_forex_data(self, base=None, symbols=None, places=None, source=None):
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

# Streamlit App
def main():
    st.title('Forex Data Query')
    st.write('Enter your options below and click on "Get Data" to query forex data.')

    # User inputs using Streamlit widgets
    base_currency = st.text_input('Base Currency (comma-separated)', 'USD')
    symbols = st.text_input('Currency Symbols (comma-separated)', 'EUR,GBP,INR,PLN')
    places = st.number_input('Decimal Places', min_value=0, value=2)
    source = st.text_input('Data Source', 'ecb')

    conn = ForexConnection(connection_name="forex")  # Pass the connection_name here
    if st.button('Get Data'):
        # Call the query_forex_data method of the connection with user inputs
        result_df = conn.query_forex_data(base=base_currency, symbols=symbols, places=places, source=source)

        if result_df is not None and not result_df.empty:
            # Display the resulting DataFrame with the exchange rates
            st.write(f'Exchange Rates (1 {base_currency} equals):')
            st.dataframe(result_df)

            # Download Button
            st.download_button(
                label="Download data as CSV",
                data=result_df.to_csv().encode('utf-8'),
                file_name='forex_data.csv',
                mime='text/csv'
            )

            # Print the final query URL
            query_params = {
                'base': base_currency,
                'symbols': symbols,
                'places': places,
                'source': source
            }
            query_url = f'https://api.exchangerate.host/latest?{"&".join(f"{key}={value}" for key, value in query_params.items() if value)}'
            st.write(f'Query URL:')
            st.code(query_url)
        else:
            st.error('Failed to retrieve data. Please check your inputs and try again.')

if __name__ == "__main__":
    main()





