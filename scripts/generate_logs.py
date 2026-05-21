import random
from faker import Faker
import pandas as pd

data = []

fake = Faker()

events = [
    "LOGIN_SUCCESS",
    "FAILED_LOGIN",
    "PASSWORD_RESET",
    "MALWARE_ALERT",
    "FIREWALL_bLOCK",
    "SUSPICIOUS_IP"
]

devices = ["Windows", "Linux", "MacOS"]
countries = ["India", "USA", "Germany", "UK", "Canada"]

for i in range(10000):
    data.append({
        "event_time": fake.date_time_this_year(),
        "user_id": random.randint(100, 999),
        "ip_address": fake.ipv4(),
        "event_type": random.choice(events),
        "device_type": random.choice(devices),
        "country": random.choice(countries),
        "severity": random.choice(["LOW", "MEDIUM", "HIGH"])
    })

df = pd.DataFrame(data)

df.to_csv("data/raw/security_logs.csv", index=False)

print("Data genarated successfully !!!! ✅")