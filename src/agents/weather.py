from uagents import Agent
import requests
weather_agent = Agent(
    name="Weather Agent",
    port=8001,
    seed="Gemini Agent secret phrase",
    endpoint=["http://localhost:8001/submit"],
)

url=f"https://mars.nasa.gov/rss/api/?feed=weather&category=insight_temperature&feedtype=json&ver=1.0&Date=2024-02-01"
response = requests.get(url)
print(response.json()["675"]["AT"]["av"])