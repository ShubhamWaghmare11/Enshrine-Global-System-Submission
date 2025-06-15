import requests
from google.adk.agents import Agent
from google.adk.tools import ToolContext
import os


def get_next_spacex_launch(tool_context:ToolContext) -> dict:
    """Fetches the enxt SpaceX Launch details."""

    try:
        launch_response = requests.get("https://api.spacexdata.com/v4/launches/next")
        launch_data = launch_response.json()

        location_response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{launch_data['launchpad']}")
        location_data = location_response.json()

        print("ERROR NOT TILL HERE")
        data = {
            "status": "success",
            "launch_date": launch_data["date_utc"],
            "location": location_data["locality"],
            "region": location_data['region'],
            "details": launch_data["details"] or "No additional details available."
        }

        tool_context.state['spacex_data'] = data
        return data

    except Exception as e:
        return {"status":"error","error_message":str(e)}


spacex_agent = Agent(
    name="spacex_agent",
    model="gemini-2.0-flash",
    description='An agent that give information about spacex latest launch',
    instruction="""
    You are the SpaceX Agent, responsible for fetching information about the next SpaceX launch. Use the SpaceX API (https://api.spacexdata.com/v5/launches/next) to retrieve details including the launch date (in UTC), time, and launchpad location. Store the extracted data in the ToolContext under the key 'launch_data' as a dictionary with fields 'date_utc', 'time_utc', and 'location'.
    Delegate yourself to Root Manager once you are done with your task.
    """,
    tools = [get_next_spacex_launch]

)