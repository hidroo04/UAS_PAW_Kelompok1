"""Test booking with proper error handling"""
import requests
import json

BASE_URL = "http://localhost:6543/api"

print("=== Testing Booking System ===\n")

# Step 1: Login
print("Step 1: Login as Alice...")
login_data = {
    "email": "alice@member.com",
    "password": "member123"
}

try:
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login Status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_result = login_response.json()
        token = login_result.get("token")
        print(f"✓ Login successful")
        print(f"Token: {token[:50]}...\n")
        
        # Step 2: Get classes
        print("Step 2: Getting available classes...")
        classes_response = requests.get(f"{BASE_URL}/classes")
        if classes_response.status_code == 200:
            classes_data = classes_response.json()
            classes = classes_data.get("data", [])
            print(f"✓ Found {len(classes)} classes\n")
            
            if classes:
                
                test_class = classes[0]
                print(f"Step 3: Attempting to book: {test_class['name']}")
                print(f"Class ID: {test_class['id']}")
                print(f"Trainer: {test_class.get('trainer', {}).get('name', 'N/A')}\n")
                
                
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                booking_data = {"class_id": test_class['id']}
                
                print(f"Sending POST to {BASE_URL}/bookings")
                print(f"Headers: {headers}")
                print(f"Data: {booking_data}\n")
                
                booking_response = requests.post(
                    f"{BASE_URL}/bookings",
                    json=booking_data,
                    headers=headers
                )
                
                print(f"Booking Status Code: {booking_response.status_code}")
                print(f"Booking Response: {json.dumps(booking_response.json(), indent=2)}")
                
                if booking_response.status_code == 200:
                    print("\n✅ BOOKING SUCCESSFUL!")
                else:
                    print(f"\n❌ BOOKING FAILED")
                    print(f"Error: {booking_response.json().get('message')}")
        else:
            print(f"Failed to get classes: {classes_response.status_code}")
    else:
        print(f"Login failed: {login_response.json()}")
        
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION ERROR: Backend server is not running!")
    print("Please start the backend server with: pserve development.ini --reload")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
