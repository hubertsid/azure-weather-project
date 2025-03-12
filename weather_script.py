import requests
import pyodbc as odbc
import os

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

CITY = "Split"
API_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"

DRIVER = "{ODBC Driver 17 for SQL Server}"  
CONN_STR = f"DRIVER={DRIVER};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}"

try:
    response = requests.get(API_URL)
    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    weather_desc = data["weather"][0]["description"]

    conn = odbc.connect(CONN_STR)
    cursor = conn.cursor()

    query = """INSERT INTO WeatherData (city, temperature, humidity, pressure, weather)
               VALUES (?, ?, ?, ?, ?)"""
    cursor.execute(query, (CITY, temperature, humidity, pressure, weather_desc))

    conn.commit()
    print("Data uploaded")

    cursor.close()
    conn.close()

except Exception as e:
    print("Error", e)