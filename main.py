import requests
from datetime import datetime
import smtplib
from time import sleep

# Enter your location to check if ISS is near you
my_latitude = 51.971748
my_longitude = 16.378634
my_location = {"lat": my_latitude, "lng": my_longitude}

# Enter an email to get info on it
email_to_get_info = "m.a.s.m@wp.pl"


# Function return True if ISS location from API is +/- 5 units away from data in "my_location" variable
def is_ISS_close():
    iss_location = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_location.raise_for_status()

    data = iss_location.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    near_lat = my_location["lat"] - 5 <= iss_latitude <= my_location["lat"] + 5
    near_lng = my_location["lng"] - 5 <= iss_longitude <= my_location["lng"] + 5
    if near_lat and near_lng:
        return True
    print("ISS is not near you")
    return False


# Function returns True if current time is between less than sunrise or more than sunset time from API
def is_nighttime():
    parameters = {"lat": my_location["lat"], "lng": my_location["lng"], "formatted": 0}
    sunrise_and_sunset_hours = requests.get(
        url="https://api.sunrise-sunset.org/json", params=parameters
    )
    sunrise_and_sunset_hours.raise_for_status()
    data = sunrise_and_sunset_hours.json()
    sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    current_hour = datetime.now().hour

    if current_hour <= sunrise_hour or current_hour >= sunset_hour:
        return True
    print("It is not night")
    return False


while True:
    if is_ISS_close() and is_nighttime():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user="matimis58@gmail.com", password="M.a.s.m1")
            connection.sendmail(
                from_addr="matimis58@gmail.com",
                to_addrs=email_to_get_info,
                msg="Subject: ISS is close to you!\n\nYou should look for it in the sky!",
            )
    sleep(60)
