import requests

SHIP_TOKEN = "apik_DP0aahKFsmvW9BJn9BSBghmV1AzZLp"
SHIP24_URL = "https://api.ship24.com/public/v1/trackers"

tracking_number = "3801753034"
def get_tracking_info(tracking_number):
    headers = {"Authorization": f"Bearer {SHIP_TOKEN}"}
    response = requests.get(f"{SHIP24_URL}/{tracking_number}", headers=headers)
    if response.status_code == 200:
       data = response.json()
       return data
    print(response.text)
    print(f"Error {response.status_code}")
    return None
tracking_data = get_tracking_info(tracking_number)

if tracking_data:
    print(tracking_data)