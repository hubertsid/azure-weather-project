import requests
import pyodbc
import datetime
import os

# 🔑 Load secrets from GitHub Actions environment variables
SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# 📍 API Configuration
CITY = "Split"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"

# 🔌 Azure SQL Connection String
DRIVER = "{ODBC Driver 17 for SQL Server}"  # Ensure this is installed in GitHub Actions
CONN_STR = f"DRIVER={DRIVER};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}"

# 📅 Get today's timestamp (12:00:00)
today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

try:
    # 🌍 Connect to OpenWeather API
    response = requests.get(API_URL)
    data = response.json()

    if response.status_code == 200:
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        weather_desc = data["weather"][0]["description"]

        # 🔌 Connect to Azure SQL
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()

        # 🔍 Check if today's record exists
        check_query = "SELECT COUNT(*) FROM WeatherData WHERE timestamp = ?"
        cursor.execute(check_query, (today,))
        result = cursor.fetchone()[0]

        if result == 0:  # Only insert if no record exists
            insert_query = """INSERT INTO WeatherData (city, temperature, humidity, pressure, weather, timestamp)
                              VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(insert_query, (CITY, temperature, humidity, pressure, weather_desc, today))
            conn.commit()
            print(f"✅ New record added: {temperature}°C, {weather_desc} - {today}")

        else:
            print("ℹ️ Today's data already exists, skipping insert.")

        cursor.close()
        conn.close()

    else:
        print(f"❌ Error fetching weather data: {data}")

except Exception as e:
    print(f"❌ Error: {e}")