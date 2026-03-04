import requests


def test_conversion(amount, from_curr, to_curr):
    url = f"http://localhost:8000/api/expenses/convert_currency/?amount={amount}&from={from_curr}&to={to_curr}"
    try:
        response = requests.get(url)
        print(f"Testing {from_curr} -> {to_curr} with amount {amount}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 20)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Test valid conversion
    test_conversion(100, "USD", "EUR")
    # Test same currency
    test_conversion(100, "USD", "USD")
    # Test invalid currency
    test_conversion(100, "USD", "INVALID")
    # Test missing amount (should fail)
    test_conversion("", "USD", "EUR")
