import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        # Launch browser in maximized state
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context with no default viewport to allow maximization
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        
        # Navigate to EaseMyTrip
        await page.goto("https://www.easemytrip.com/")
        
        # Wait for page to load
        await page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(2)
        
        # Click on Round Trip button
        try:
            # Using the exact button/label visible in the UI
            await page.click("text=Round Trip", timeout=10000)
            print("Clicked on Round Trip successfully")
        except:
            try:
                # Try clicking using CSS selector for the Round Trip label
                await page.click("label:has-text('Round Trip')")
                print("Clicked on Round Trip using label selector")
            except:
                try:
                    # Try the ID of the radio button
                    await page.click("#rdoRoundTrip", force=True)
                    print("Clicked on Round Trip using force click")
                except Exception as e:
                    print(f"Failed to click Round Trip: {e}")
        
        # Wait for 2 seconds
        await asyncio.sleep(2)
        
        # Close the browser
        await browser.close()
        print("Browser closed")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())