import requests
import time

print("🧪 Testing Honeypot with Real Timestamps")
print("="*50)

# Test 1: Make a fresh login attempt
login_url = "http://127.0.0.1:5000/login"

test_logins = [
    ("admin", "admin123"),
    ("testuser", "password456"),
    ("john_doe", "mypassword789")
]

for username, password in test_logins:
    print(f"\n📝 Sending login: {username}/{password}")
    response = requests.post(login_url, data={
        'username': username,
        'password': password
    })
    print(f"   ✓ Login attempt sent")
    time.sleep(1)

# Test 2: Check the API for timestamps
print("\n\n📊 Checking API for Real Timestamps:")
api_url = "http://127.0.0.1:5000/api/attempts"
response = requests.get(api_url)
data = response.json()

if data:
    print("\n✅ Recent attempts with timestamps:")
    for attempt in data[:5]:  # Show first 5
        print(f"   ID: {attempt['id']} | Time: {attempt['timestamp']} | User: {attempt['username']}")
else:
    print("❌ No attempts found")

print("\n" + "="*50)
print("✨ If you see real timestamps (like '2026-05-04 14:37:37'), it's working!")
print("   If you still see 'Local', restart the server and try again.")