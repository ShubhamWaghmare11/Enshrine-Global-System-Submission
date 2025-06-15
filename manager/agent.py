from google.adk.agents import LlmAgent
from .sub_agents.spacex_agent.agent import spacex_agent
from .sub_agents.weather_agent.agent import weather_agent
from .sub_agents.newsapi_agent.agent import news_agent
from .sub_agents.coingecko_agent.agent import coingecko_agent



root_agent = LlmAgent(
    name="manager",
    model="gemini-2.0-flash",
    description='Manager Agent',
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - spacex_agent
    - weather_agent
    - news_agent
    - coingecko_agent

    delegate back to yourself after sub agent is done.
    """,
    sub_agents=[spacex_agent,weather_agent,news_agent, coingecko_agent]

)