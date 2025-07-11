import requests

# Define the endpoint URL
url = "http://localhost:5000/api/v1/items"

# Open the NDJSON file in binary mode
with open("data/history.ndjson", "rb") as f:
    data = f.read()

# Define the headers
headers = {
    "Content-Type": "application/x-ndjson"
}

# Make the POST request
response = requests.post(url, headers=headers, data=data)

# Print the response
print("Status code:", response.status_code)
print("Response body:", response.text)
