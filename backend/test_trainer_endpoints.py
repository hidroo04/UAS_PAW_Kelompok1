"""
Test trainer endpoints - Get classes and remove members
"""
import requests
import json

BASE_URL = "http://localhost:6543"

print("\n" + "=" * 60)
print("TESTING TRAINER ENDPOINTS")
print("=" * 60)

# 1. Login as John Smith (trainer)
print("\n1. Login as trainer (John Smith)...")
login_data = {
    "email": "john.trainer@gym.com",
    "password": "trainer123"
}

response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
if response.status_code == 200:
    result = response.json()
    token = result.get('token')
    user = result.get('data')
    print(f"✓ Login successful: {user['name']} ({user['role']})")
    print(f"Token: {token[:50]}...")
else:
    print(f"✗ Login failed: {response.status_code}")
    print(response.text)
    exit(1)

# 2. Get trainer's classes
print("\n2. Getting trainer's classes...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get(f"{BASE_URL}/api/trainer/classes", headers=headers)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    print(f"Response Status: {result['status']}")
    print(f"Classes Count: {result['count']}\n")
    
    classes = result['data']
    for i, cls in enumerate(classes, 1):
        print(f"{i}. {cls['name']}")
        print(f"   Schedule: {cls['schedule']}")
        print(f"   Capacity: {cls['enrolled_count']}/{cls['capacity']}")
        print(f"   Available slots: {cls['available_slots']}")
        
        if cls['members']:
            print(f"   Members enrolled:")
            for member in cls['members']:
                print(f"      - {member['name']} ({member['email']}) - Booking ID: {member['booking_id']}")
        else:
            print(f"   No members enrolled yet")
        print()
    
    # Test removing a member if any exists
    if classes and classes[0]['members']:
        print("\n3. Testing remove member functionality...")
        first_class = classes[0]
        first_member = first_class['members'][0]
        
        print(f"\nAttempting to remove {first_member['name']} from {first_class['name']}...")
        print(f"Booking ID: {first_member['booking_id']}")
        print("\n⚠️  This is a destructive test - commenting out actual deletion")
        print("To test deletion, uncomment the code below:")
        print(f"# DELETE /api/trainer/classes/{first_class['id']}/members/{first_member['booking_id']}")
        
        # Uncomment below to actually test deletion
        # confirm = input("\nType 'yes' to proceed with deletion: ")
        # if confirm.lower() == 'yes':
        #     delete_response = requests.delete(
        #         f"{BASE_URL}/api/trainer/classes/{first_class['id']}/members/{first_member['booking_id']}",
        #         headers=headers
        #     )
        #     print(f"Delete Status: {delete_response.status_code}")
        #     print(f"Response: {delete_response.json()}")
else:
    print(f"Error: {response.json()}")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60 + "\n")
