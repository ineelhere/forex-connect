import streamlit as st
from forex_connection import *

# Streamlit App
def forexUI():
    st.title('DEMO 🕹️')
    st.write('Enter your options below and click on `Get Data` to query forex data.')

    col1, col2 = st.columns(2)

    # Create an instance of the forex_connection class
    conn = st.experimental_connection('forex', type=forex_connection)

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
