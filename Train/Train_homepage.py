from playwright.sync_api import sync_playwright
import time

def launch_and_navigate():
    with sync_playwright() as p:
        # Launch browser in non-headless mode with args to start maximized
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create a new browser context without viewport restrictions
        context = browser.new_context(
            no_viewport=True
        )
        
        # Create a new page
        page = context.new_page()
        
        print("Browser launched in maximized mode")
        
        # Navigate to EaseMyTrip
        print("Navigating to EaseMyTrip.com...")
        page.goto("https://www.easemytrip.com/", wait_until="load", timeout=60000)
        
        print("Successfully navigated to EaseMyTrip.com")
        print(f"Page title: {page.title()}")
        
        # Wait for the page elements to load
        time.sleep(5)
        
        # Click on the Train module - trying multiple selectors
        print("Clicking on Train module...")
        try:
            # Try clicking by text content
            page.click("text=Trains", timeout=15000)
            print("Clicked using text=Trains")
        except Exception as e:
            print(f"First attempt failed: {e}")
            try:
                # Alternative: Direct navigation to trains page
                print("Trying direct navigation...")
                page.goto("https://www.easemytrip.com/railways/", wait_until="load", timeout=60000)
            except Exception as e2:
                print(f"Direct navigation failed: {e2}")
        
        # Wait a bit for the page to settle
        time.sleep(3)
        
        print("Successfully navigated to Train homepage")
        print(f"Current URL: {page.url}")
        print(f"Page title: {page.title()}")
        
        # Keep the browser open for 10 seconds to view the train page
        time.sleep(10)
        
        # Close the browser
        browser.close()
        print("Browser closed")

if __name__ == "__main__":
    launch_and_navigate()