import requests

# Test GET my bookings
response = requests.get('http://localhost:6543/api/bookings/my')
print("Status Code:", response.status_code)
print("Response:", response.text)
print("\nJSON:", response.json() if response.status_code == 200 else "Error")
