import requests
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY")

CITY = "Warsaw"
TMP_FOLDER = "/tmp/weather_reports"
os.makedirs(TMP_FOLDER, exist_ok=True)

def fetch_weather_data():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return {
        "city": CITY,
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["main"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def generate_report_pdf(data: dict):
    filename = f"{TMP_FOLDER}/weather_report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    c.drawString(100, 800, f"Weather Report for {data['city']}")
    c.drawString(100, 770, f"Temperature: {data['temp']}°C")
    c.drawString(100, 750, f"Humidity: {data['humidity']}%")
    c.drawString(100, 730, f"Condition: {data['weather']}")
    c.drawString(100, 710, f"Time: {data['timestamp']}")
    c.save()
    print(f"PDF saved to: {filename}")
