import requests

# Run script on startup for a briefing


def main():

    # enter iPad model, stock symbols, lat & long
    
    iPad_model = ""
    stock_list = [None]
    lat, long = "", ""

    ios_checker(iPad_model)
    print('\n')
    stock_quick_view(stock_list)
    print('\n')
    weather_data(lat, long)
    
    return

def ios_checker(device):

    """Utilizes the IPSW api to find which iOS versions Apple is signing off on for passed device."""
    
    url = 'https://api.ipsw.me/v4/device/' + device + '?type=ipsw'
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)

    data = r.json()
    versions = data['firmwares']

    output = f'The currently supported iOS version for {device} is: ' \
        f'{", ".join([version["version"] for version in versions if version["signed"]])}'

    print('\n')
    print(output)
    return


def stock_quick_view(symbols):

    """Utilizes the aplhavantage API to find stock prices for symbols passed."""
    
    # enter alphavantage api key:
    key = ""

    for symbol in symbols:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + symbol + \
              '&apikey=' + key

        headers = {'Accept': 'application/json'}
        r = requests.get(url, headers=headers)
        data = r.json()
        top = data['Meta Data']
        latest = top['3. Last Refreshed'][0:10]
        trading_days = data['Time Series (Daily)']
        day = trading_days[latest]
        price = day['4. close']

        print(f'Latest price for {symbol}: {float(price)}')

    return


def weather_data(lat, long):

    """Utilizes the NWS API to find 5 day forecast."""

    lat_long = 'https://api.weather.gov/points/' + lat + ',' + long
    headers = {'Accept': 'application/json'}
    r = requests.get(lat_long, headers=headers)
    data = r.json()
    lat_long_top = data['properties']
    url = lat_long_top['forecast']

    forecast_data = requests.get(url, headers=headers).json()

    forecast_top = forecast_data['properties']
    days = forecast_top['periods']

    for num in range(0, 10, 2):
        print(f"{days[num]['name']}'s temp: {days[num]['temperature']}")
        print(f"{days[num]['name']}'s wind: {days[num]['windSpeed']} from the {days[num]['windDirection']}")
        print(f"{days[num]['name']}'s forecast: {days[num]['detailedForecast']}")
        print('\n')

    return


if __name__ == '__main__':
    main()
