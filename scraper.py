import os
import asyncio
from stagehand import Stagehand

# # Set the MODEL_API_KEY environment variable
os.environ["MODEL_API_KEY"] = "MODEL_API_KEY"

# Environment Variables
os.environ["BROWSERBASE_API_KEY"] = "BROWSERBASE_API_KEY"
os.environ["BROWSERBASE_PROJECT_ID"] = "BROWSERBASE_PROJECT_ID"

async def quick_scrape(pid):
    stagehand = Stagehand()

    # Example: Sending a POST request to create a new browser session
    response = await stagehand.post("/browser/sessions", json={"permit_id": pid})
    print(response)

    # Example: Sending a GET request to retrieve data
    data = await stagehand.get("/browser/data")
    print(data)

if __name__ == "__main__":
    try:
        data = asyncio.run(quick_scrape("202412345678"))
        print(f"Final Scraped Data: {data}")
    except Exception as e:
        print(f"Scrape failed: {e}")
