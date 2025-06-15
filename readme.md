# Multi-Agent AI System Using Google ADK

## Overview
This project implements a **multi-agent system** that processes user goals by delegating tasks to specialized sub-agents. The Manager agent creates a plan, routes data between sub-agents, and iterates if the goal isn’t met.

It supports both:
- **Single-agent queries**: e.g., "Get crypto market data"
- **Multi-agent queries**: e.g., "Find the next SpaceX launch, check weather, summarize delays"

---

## System Flow

The **Manager agent** orchestrates tasks:

- **Single-agent query**  
  → e.g., "Get crypto market data"  
  → Routes directly to: `CoinGecko Agent`

- **Multi-agent query**  
  → e.g., "Find the next SpaceX launch, check weather, summarize delays"  
  → Routes:
  ```
  SpaceX Agent → Weather Agent → NewsAPI Agent → (optional) CoinGecko Agent → Manager
  ```

- **Data flow example**:
  ```
  SpaceX provides → [launch date, location]  
  Weather uses location → [weather data]  
  NewsAPI uses date/weather → [launch delay news]  
  CoinGecko (optional) → [market impact]
  ```

- The **Manager retries** if any sub-agent fails (e.g., Weather API returns no data).

---

## Agent Logic

### Manager Agent (agent.py):

- **Input**: User goal  
  _(e.g., "Find SpaceX launch, check weather, summarize delays")_
- **Logic**: Parses the goal, creates an execution plan, routes data, handles retries.
- **Output**: Final result  
  _(e.g., "Launch on 2025-06-20 at Cape Canaveral, clear weather, low delay likelihood")_

---

### Sub-Agents

#### SpaceX Agent (`sub_agents/spacex_agent/agent.py`)
- **Input**: None  
- **Logic**: Fetches next launch using SpaceX API  
- **Output**:
  ```json
    {
    "get_next_spacex_launch_response": {
        "details": "No additional details available.",
        "launch_date": "2022-11-01T13:41:00.000Z",
        "location": "Cape Canaveral",
        "region": "Florida",
        "status": "success"
    }
    }
  ```



#### Weather Agent (`sub_agents/weather_agent/agent.py`)
- **Input**: Location to fetch weather of.
- **Logic**: Fetches weather using OpenWeatherMap API.
- **Output**:
  ```json
  {
    "conditions": {...},
    "temp_c": 27.1,
    ...
  }
  ```


#### NewsAPI Agent (`sub_agents/newsapi_agent/agent.py`)
- **Input**: query, page_num and total_news.
- **Logic**: Fetches news about regarding the given query ex. Donald trump.
- **Output**: 
    ```json
    {
    "get_news_response": {
    "content": "string",
    "description": "string",
    "source": "string",
    "title": "string"
    }
    }
    ```


#### CoinGecko Agent (`sub_agents/coingecko_agent/agent.py`)
- **Input**: the coin id of whom user wants price and market cap info.
- **Logic**: Fetches crypto market data using CoinGecko API.
- **Output**: 
    ```json
    {
    "status": "success",
    "coin_id": "bitcoin",
    "date": "current",
    "price_usd": 105672.69962498271,
    "market_change_24h": 0.6559815372632949
    }
    ```

---


## APIs Used


| API               | URL                                                                  | API Key Required |
|-------------------|----------------------------------------------------------------------|------------------|
| **Google ADK**    | ---                                                                  | ✅ Yes           |
| **SpaceX**        | https://api.spacexdata.com/v4/launches/next                          | ❌ No            |
| **WeatherAPI**    | https://api.openweathermap.org/data/2.5/weather                      | ✅ Yes           |
| **NewsAPI**       | https://newsapi.org/v2/everything                                    | ✅ Yes           |
| **CoinGecko**     | https://api.coingecko.com/api/v3/coins/markets                       | ❌ No            |


Get Keys:
- [GoogleADK](https://aistudio.google.com/apikey)
- [WeatherAPI](https://www.weatherapi.com/)
- [NewsAPI](https://newsapi.org/)

---



## Setup Instructions

1. **Clone the repository or unzip the project folder.**
2. **Install Python 3.10+.**
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Create `.env` in root**:
   ```
   GOOGLE_GENAI_USE_VERTEXAI= 0
   GOOGLE_API_KEY= your_google_api_key
   OPENWEATHERMAP_API_KEY= your_openweathermap_key
   NEWSAPI_API_KEY= your_newsapi_key
   ```

---

## Running the System

### Start the main agent (planner agent):
```bash
adk run manager 
```

### Example Usage:
```python
manager_agent("Find the next SpaceX launch, check weather, summarize if it may be delayed")
```

---

### Run evaluations:
```bash
python eval.py
```

---
## Evaluations

Available in `eval.py`:

- **Test 1**: Goal satisfaction for multi-agent pipeline  
  _(SpaceX → Weather → NewsAPI)_

- **Test 2**: Agent trajectory validation  
  _(Ensures correct data flow between agents)_

---

## Folder Structure

```
project_root/
│
├── agent.py                   # Manager agent
├── eval.py                    # Evaluations
├── .env                       # API keys
├── sub_agents/
│   ├── spacex_agent/
│   │   └── agent.py
│   ├── weather_agent/
│   │   └── agent.py
│   ├── newsapi_agent/
│   │   └── agent.py
│   └── coingecko_agent/
│       └── agent.py
```

---

