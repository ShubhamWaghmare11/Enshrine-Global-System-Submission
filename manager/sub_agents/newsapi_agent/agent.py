import requests
from google.adk.agents import Agent
from google.adk.tools import ToolContext
import os
from dotenv import load_dotenv

load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


def get_news(query: str, tool_context: ToolContext, total_news: int = 10,page_num: int = 1) -> dict:
    """Fetches the enxt SpaceX Launch details."""

    try:
        response = requests.get(f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}&sortBy=publishedAt&language=en&pageSize={total_news}&page={page_num}")
        news_data = response.json()

        tool_context.state['news_data'] = news_data
        return news_data


    except Exception as e:
        return {"status":"error","error_message":str(e)}


news_agent = Agent(
    name="news_agent",
    model="gemini-2.0-flash",
    description='An agent that give retrieves news based on given query',
    instruction="""
    You are the newsApi Agent, responsible for fetching news about the given topic. Use the get_news tool to retrieve the news including the title, source, description, content.
    """,
    tools = [get_news]

)