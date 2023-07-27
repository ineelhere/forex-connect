import requests
import pandas as pd

def query(base=None, symbols=None, amount=None, callback=None, places=None, source=None):
    base_url = 'https://api.exchangerate.host/latest'
    params = {'base': 'USD'}  # Assuming base currency is always USD

    # Add optional parameters to the request if provided
    if symbols:
        params['symbols'] = symbols
    if amount:
        params['amount'] = amount
    if callback:
        params['callback'] = callback
    if places:
        params['places'] = places
    if source:
        params['source'] = source

    response = requests.get(base_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Extract rates data from the response
        rates = data.get('rates', {})

        # Convert the rates data to a DataFrame
        df = pd.DataFrame.from_dict(rates, orient='index', columns=['Rate'])

        # If amount is provided, calculate the converted values and add to DataFrame
        if amount:
            df['Converted Amount'] = df['Rate'] * amount

        return df
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

# Example usage of the function:
if __name__ == "__main__":
    # Call the function with various options to query forex data
    result_df = query(symbols='EUR,GBP,INR,PLN', amount=100, places=2, source='ecb')

    # Print the DataFrame
    print(result_df)
