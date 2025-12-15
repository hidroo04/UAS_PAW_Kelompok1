import requests

# First login as Jane
login_url = 'http://127.0.0.1:6543/api/auth/login'
profile_url = 'http://127.0.0.1:6543/api/auth/me'

print("🔐 Logging in as Jane Member...")
login_response = requests.post(login_url, json={
    'email': 'member@gym.com',
    'password': 'member123'
})

if login_response.status_code == 200:
    data = login_response.json()
    token = data['data']['token']
    print(f"✅ Login successful! Token: {token[:30]}...")
    
    # Get user profile with token
    print("\n👤 Getting user profile...")
    headers = {'Authorization': f'Bearer {token}'}
    profile_response = requests.get(profile_url, headers=headers)
    
    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        print(f"\n✅ Profile data:")
        print(f"   Name: {profile_data['data']['name']}")
        print(f"   Email: {profile_data['data']['email']}")
        print(f"   Role: {profile_data['data']['role']}")
        
        if 'membership_plan' in profile_data['data']:
            print(f"   🎫 Membership Plan: {profile_data['data']['membership_plan']}")
            print(f"   📊 Membership Status: {profile_data['data']['membership_status']}")
            if 'membership_expiry' in profile_data['data']:
                print(f"   📅 Membership Expiry: {profile_data['data']['membership_expiry']}")
        else:
            print("   ⚠️ No membership information found")
    else:
        print(f"❌ Profile request failed: {profile_response.status_code}")
        print(profile_response.text)
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(login_response.text)
