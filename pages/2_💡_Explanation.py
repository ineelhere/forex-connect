import streamlit as st
from footer import *

st.title("Forex 💸 Connect")
st.text("Explore Foreign Currency Exchange rates 💰 in real-time")

st.header("📖 Technical Explanation")

tab1, tab2 = st.tabs([
    "🧰 Defining the connection class",
    "🚀 Implementation with st.experimental_connection",
])

with tab1:
    st.markdown("""

    The code defines a Streamlit connection class named `forex_connection`, which is a custom experimental connection to fetch foreign exchange rate data.

    The whole script can be located in the `forex_connection.py` file in the root directory of this application

    Let's go through the code step by step:

    ```python
    import streamlit as st
    from streamlit.connections import ExperimentalBaseConnection
    import pandas as pd
    import requests

    ```
    The code imports the necessary libraries:
    - `streamlit`: The main library used for creating Streamlit applications.
    - `ExperimentalBaseConnection`: This is the base class for creating custom experimental connections in Streamlit.
    - `pandas as pd`: A widely used library for data manipulation and analysis.
    - `requests`: A library used for making HTTP requests to APIs.

    ```python
    class forex_connection(ExperimentalBaseConnection):
        def __init__(self, connection_name, **kwargs):
            super().__init__(connection_name, **kwargs)

        def _connect(self):
            # This method is called when the connection is initialized.
            # For this example, we don't need any setup or initialization,
            # so we leave it empty.
            pass

    ```
    A custom connection class, `forex_connection`, is defined. It subclasses `ExperimentalBaseConnection`, and it is used to establish a connection with the data source and fetch foreign exchange rate data.

    The constructor (`__init__`) of the `forex_connection` class is defined. It takes a `connection_name` argument along with any other keyword arguments (`**kwargs`). The `connection_name` is passed to the superclass constructor using `super().__init__(connection_name, **kwargs)`.

    The `_connect` method is defined, but it is left empty. The `_connect` method is called when the connection is initialized. For this example, no setup or initialization is required, so the method is left empty.

    ```python
        def get_data_source_df(self):
            # Return the DataFrame with the IMF data
            data = {
                'Abbreviation': ['imf', 'rba', 'boc', 'snb', 'cbr', 'nbu', 'bnro', 'boi', 'nob', 'cbn', 'ecb'],
                'Full_Name': ['International Monetary Fund', 'Reserve Bank of Australia', 'Bank of Canada', 'Swiss National Bank',
                            'Central Bank of Russia', 'National Bank of Ukraine', 'National Bank of Romania', 'Bank Of Israel',
                            'Norges Bank', 'Central Bank of Nigeria', 'European Central Bank']
            }
            return pd.DataFrame(data)

    ```
    The `get_data_source_df` method is defined, which returns a DataFrame containing the names and abbreviations of various central banks and international monetary organizations. The data is hardcoded into a dictionary and then converted into a pandas DataFrame.

    ```python
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
    ```
    The `query` method is decorated with `st.cache_data()`, indicating that the results of this method should be cached for faster access during the application's lifetime. This method is responsible for fetching the foreign exchange rate data using the 'exchangerate.host' API.

    - The method takes four optional arguments: `base`, `symbols`, `places`, and `source`. These arguments allow users to customize their queries by specifying the base currency, target symbols, decimal places, and data source, respectively.

    - The method constructs the API URL based on the provided arguments (or using default values if not provided).

    - It then makes an HTTP GET request to the API using the `requests` library and checks if the response status code is 200 (indicating a successful request).

    - If the request is successful, it extracts the exchange rate data from the response, converts it into a DataFrame, and returns it.

    - If the request fails (status code other than 200), it displays an error message using Streamlit's `st.error()` function and returns `None`.
    """)
                
with tab2:
    st.markdown("""
    This code is a Streamlit app that uses the custom `forex_connection` class to query and display foreign exchange rate data based on user inputs. The app provides input fields for the user to specify the base currency, target currency symbols, decimal places, and data source. Upon clicking the "Get Data" button, the app fetches the exchange rate data using the custom connection and displays the results in a DataFrame. The user can also download the data as a CSV file, and the app prints the final query URL for reference.

    The whole script can be located in the `forexUI.py` file in the root directory of this application

    Let's go through the code step by step:

    ```python
    import streamlit as st
    from forex_connection import *
    ```
    The code imports the necessary libraries, including Streamlit (`streamlit`) and the custom connection class `forex_connection` from the `forex_connection` module.

    ```python
    # Streamlit App
    def forexUI():
        st.title('DEMO 🕹️')
        st.write('Enter your options below and click on `Get Data` to query forex data.')

        col1, col2 = st.columns(2)
    ```
    A Streamlit app function named `forexUI` is defined. This function sets up the user interface for the app and handles user interactions.

    The Streamlit app is organized into two columns (`col1` and `col2`) using the `st.columns()` function. The left column (`col1`) contains input fields for the user to specify the base currency, target currency symbols, decimal places, and data source. The right column (`col2`) will display the results of the data query.

    ```python
        # Create an instance of the forex_connection class
        conn = st.experimental_connection('forex', type=forex_connection)

    ```
    An instance of the `forex_connection` class is created using the `st.experimental_connection()` function. This allows the app to utilize the custom connection to fetch foreign exchange rate data.

    ```python
        with col1:
        # User inputs using Streamlit widgets
        base_currency = st.text_input('Base Currency', 'USD')
        symbols = st.text_input('Currency Symbols (comma-separated)', 'USD,EUR,INR')
        places = st.number_input('Decimal Places', min_value=0, value=2)
        data_source_df = conn.get_data_source_df()
        data_source = st.selectbox('Data Source', data_source_df['Full_Name'], index=0)

    # Get the abbreviation based on the selected full name from the DataFrame
    selected_abbreviation = data_source_df[data_source_df['Full_Name'] == data_source]['Abbreviation'].iloc[0]
    
    if st.button('Get Data'):
        with col2:
            # Call the query method of the connection with user inputs
            result_df = conn.query(base=base_currency, symbols=symbols, places=places, source=selected_abbreviation)

            if result_df is not None and not result_df.empty:
                # Display the resulting DataFrame with the exchange rates
                st.write(f'Exchange Rates (1 {base_currency} equals):')
                st.dataframe(result_df)
    ```
    In the left column (`col1`), Streamlit widgets (text inputs and a selectbox) are used to capture user inputs for base currency, currency symbols, decimal places, and data source. The available data sources are fetched from the `get_data_source_df()` method of the custom connection.

    The selected data source's abbreviation is extracted from the DataFrame to be used in the query.

    If the user clicks the "Get Data" button, the app proceeds to the right column (`col2`).

    The `query` method of the custom connection (`conn`) is called with the user inputs (base currency, currency symbols, decimal places, and data source abbreviation) to fetch the exchange rate data.

    If the query is successful and the result DataFrame (`result_df`) is not empty, the exchange rate data is displayed in a DataFrame using `st.dataframe()`.

    ```python
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
                    'source': selected_abbreviation
                }
                query_url = f'https://api.exchangerate.host/latest?{"&".join(f"{key}={value}" for key, value in query_params.items() if value)}'
                st.success(f'Query URL: {query_url}')
            else:
                st.error('Failed to retrieve data. Please check your inputs and try again.')

    # Run the Streamlit app
    if __name__ == '__main__':
        forexUI()
    ```
    A "Download data as CSV" button is provided, allowing the user to download the data as a CSV file.

    The final query URL used to fetch the data is displayed at the bottom of the right column (`col2`) using `st.success()`.

    If the query fails or the result DataFrame is empty, an error message is displayed using `st.error()`.


                """)

st.info("Now that the connection is ready, please feel free to modify/customise it and accordingly implement it's features! 😊")

footer()