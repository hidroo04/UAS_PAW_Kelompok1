"""
Direct test untuk debug authentication issue
"""
import sys
sys.path.insert(0, 'd:\\UAS_PAW_Kelompok1\\backend')

from app.utils.auth import create_jwt_token, decode_jwt_token, get_token_from_header
from app.config import config

print(f"JWT Secret Key: {config.JWT_SECRET_KEY}")
print(f"JWT Algorithm: {config.JWT_ALGORITHM}")

# Test create token
print("\n=== Creating Token ===")
token = create_jwt_token(user_id=57, email='alice@member.com', role='member')
print(f"Token created: {token[:50]}...")

# Test decode token
print("\n=== Decoding Token ===")
try:
    payload = decode_jwt_token(token)
    print(f"Token decoded successfully!")
    print(f"Payload: {payload}")
except Exception as e:
    print(f"ERROR decoding token: {e}")
