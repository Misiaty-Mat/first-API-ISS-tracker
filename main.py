import requests

# Acquiring data form API endpoint.
response = requests.get(url="http://api.open-notify.org/iss-now.json")

# Raise error if request has problem getting data
response.raise_for_status()

# Converting to JSON format
data = response.json()

latitude = data["iss_position"]["latitude"]
longitude = data["iss_position"]["longitude"]

print(f"ISS is currently at:\nLatitude: {latitude}\nLongitude: {longitude}")
