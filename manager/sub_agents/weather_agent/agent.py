from google.adk.agents import Agent
from google.adk.tools import ToolContext
import requests
from dotenv import load_dotenv
import os

load_dotenv()

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

def get_current_weather(location: str,tool_context:ToolContext) -> dict:
    try:
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={location}")
        data = response.json()
        data = {"status":"success","location":location,"weather_data":data['current']}
        tool_context.state['weather_data'] = data
        return data
    
    except Exception as e:
        return {"status":"failure","message":e}
    


weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    description="returns the weather data for particular location using get_current_weather tool",
    instruction="""
        You are the weather Agent, responsible for fetching information about the weather for particular location. 
        Use the get_current_weather tool to retrieve details including 
        the temperature (celcius and fahrenheit) wind, cloud, humidity.
    """,
    tools=[get_current_weather]
)