import requests
import json


def fetch_api_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return None


def extract_btc_prices(data):
    try:
        bpi = data["bpi"]
        result = {}
        for currency, info in bpi.items():
            result[currency] = info["rate"]
        return result
    except KeyError:
        print("Unexpected JSON structure.")
        return {}


def save_report(prices, filename="btc_price_report.txt"):
    with open(filename, "w") as f:
        f.write("Bitcoin Price Report\n")
        f.write("-------------------------\n")
        for currency, rate in prices.items():
            f.write(f"{currency}: {rate}\n")
    print(f"Report saved to {filename}")


def keyword_filter(data, keyword):
    print(f"\n🔍 Filtering JSON keys with keyword: {keyword}")

    def search(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if keyword.lower() in k.lower():
                    print(f"{k}: {v}")
                search(v)
        elif isinstance(d, list):
            for item in d:
                search(item)

    search(data)


if __name__ == "__main__":
    print(" Bitcoin Price Index Fetcher")

    use_custom = input("Do you want to enter a custom API URL? (y/n): ").lower()
    if use_custom == 'y':
        api_url = input("Enter API URL: ")
    else:
        api_url = "https://api.coindesk.com/v1/bpi/currentprice.json"

    data = fetch_api_data(api_url)

    if data:
        prices = extract_btc_prices(data)
        if prices:
            print("\nBitcoin Price Report\n-------------------------")
            for currency, rate in prices.items():
                print(f"{currency}: {rate}")
            save_report(prices)

        # Bonus: filter keys
        keyword = input("\nEnter keyword to filter JSON keys (or press Enter to skip): ").strip()
        if keyword:
            keyword_filter(data)
