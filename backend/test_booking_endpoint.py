import requests

print("=== Testing Book Class Endpoint ===\n")

# Login as member
login_response = requests.post('http://localhost:6543/api/auth/login', 
                               json={'email': 'alice@member.com', 'password': 'member123'})

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
    exit(1)

token = login_response.json()['token']
print(f"✓ Login successful")
print(f"Token: {token[:30]}...\n")

# Get available classes
classes_response = requests.get('http://localhost:6543/api/classes')
classes = classes_response.json()['data']
print(f"✓ Found {len(classes)} classes\n")

if len(classes) == 0:
    print("❌ No classes available")
    exit(1)

# Try to book the first class
class_to_book = classes[0]
print(f"Attempting to book: {class_to_book['name']}")
print(f"Class ID: {class_to_book['id']}")
print(f"Schedule: {class_to_book['schedule']}\n")

# Make booking request
headers = {'Authorization': f'Bearer {token}'}
booking_response = requests.post('http://localhost:6543/api/bookings',
                                json={'class_id': class_to_book['id']},
                                headers=headers)

print(f"Status Code: {booking_response.status_code}")
result = booking_response.json()
print(f"Response Status: {result.get('status')}")
print(f"Message: {result.get('message')}")

if result.get('status') == 'success':
    print("\n✅ BOOKING SUCCESS!")
    print(f"Booking ID: {result['data']['id']}")
else:
    print("\n❌ BOOKING FAILED!")
    if 'data' in result:
        print(f"Details: {result['data']}")
