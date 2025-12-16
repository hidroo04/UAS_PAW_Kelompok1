import requests

# Login
print("=== Testing My Bookings Endpoint ===")
r = requests.post('http://localhost:6543/api/auth/login', 
                  json={'email': 'alice@member.com', 'password': 'member123'})

token = r.json()['token']
print(f"✓ Login successful, token: {token[:30]}...")

# Get my bookings
headers = {'Authorization': f'Bearer {token}'}
r2 = requests.get('http://localhost:6543/api/bookings/my', headers=headers)

print(f"\nStatus Code: {r2.status_code}")
data = r2.json()
print(f"Response Status: {data.get('status')}")
print(f"Bookings Count: {data.get('count', 0)}")

if data.get('data'):
    print(f"\n✓ SUCCESS! Found {len(data['data'])} bookings")
    for i, booking in enumerate(data['data'], 1):
        print(f"{i}. {booking['class']['name']} - {booking['class']['schedule']}")
else:
    print("\nNo bookings found or ERROR")
    print(f"Message: {data.get('message', 'N/A')}")
