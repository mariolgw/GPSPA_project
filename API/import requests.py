import requests

# Step 1: Generate the Access Token
REFRESH_TOKEN = "AMf-vBxBvVKDdIToXLEthMXkFVFejxG04g7Ei6S2WThFRLnmWIxzOKxEvl-zRh08BD-yBJwZT-CfGR2SBLe-qcFvxR20t8l7nLaw5a1c-icB5NplCQMdyrCLaFBNItj1JF_3AJyKUYtudsODhRV5AQOLJU92aUH330XVZFQ9OMo3fRBCcW3TQpU-4zjysTUkkM7JeKYiUyA4pTtMZ3N6Gkmintr1iDvvkpU2zWLXJlPIS0QgRJzn_oSjGG3EKWAhQKcEtXm0tMWp6rKW0m0EdtLM0EW4j5qjTHWPoanUOSnracLdt8OOB6TMdDOg7xGYxC6F-bb1ekf0TC-icTlQ00AEm1QdxeEHYZzx0b7I8u_Ek2k0qe7QAVE"
TOKEN_URL = "https://api.mobilitydatabase.org/v1/tokens"

token_response = requests.post(
    TOKEN_URL,
    headers={"Content-Type": "application/json"},
    json={"refresh_token": REFRESH_TOKEN}
)

if token_response.status_code == 200:
    access_token = token_response.json().get("access_token")
else:
    print("Failed to get access token")
    print("Status Code:", token_response.status_code)
    print("Response Content:", token_response.text)
    exit()

# Step 2: Use the Access Token to make the API request
BASE_URL = "https://api.mobilitydatabase.org/v1/get/feeds"
FEED_ID = "tld-716"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(f"{BASE_URL}/{FEED_ID}", headers=headers)

print("Status Code:", response.status_code)
print("Response Content:", response.text)