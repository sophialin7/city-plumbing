import os
import asyncio
from stagehand import Stagehand

# # Set the MODEL_API_KEY environment variable
os.environ["MODEL_API_KEY"] = "MODEL_API_KEY"

# Environment Variables
os.environ["BROWSERBASE_API_KEY"] = "BROWSERBASE_API_KEY"
os.environ["BROWSERBASE_PROJECT_ID"] = "BROWSERBASE_PROJECT_ID"

async def quick_scrape(pid):

    # initialize instance of stagehand
    stagehand = Stagehand()

    page = stagehand.pages()[0]

    await page.goto("https://stagehand.dev")
    
    # Navigate and interact with the page
    await page.act("https://sfdbi.org/dbipts")  
    await page.act({"permit_search": pid})  
    
    # 3. Extract specific data for your Knowledge Graph
    result = await page.extract({
        "status": "the current status of the permit",
        "description": "a brief description of the permit",
        "valuation": "the valuation of the permit"
    })
    
    return result

if __name__ == "__main__":
    try:
        data = asyncio.run(quick_scrape("202412345678"))
        print(f"Final Scraped Data: {data}")
    except Exception as e:
        print(f"Scrape failed: {e}")
