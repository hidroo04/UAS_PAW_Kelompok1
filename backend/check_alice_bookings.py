import requests

# Login
r = requests.post('http://localhost:6543/api/auth/login', 
                  json={'email': 'alice@member.com', 'password': 'member123'})
token = r.json()['token']

# Get my bookings
r2 = requests.get('http://localhost:6543/api/bookings/my', 
                  headers={'Authorization': f'Bearer {token}'})
bookings = r2.json()['data']

print(f'Total bookings for Alice: {len(bookings)}\n')
for i, b in enumerate(bookings, 1):
    print(f'{i}. {b["class"]["name"]} (Booking ID: {b["id"]})')
    print(f'   Schedule: {b["class"]["schedule"]}')
    print(f'   Trainer: {b["class"]["trainer"]["name"]}\n')
