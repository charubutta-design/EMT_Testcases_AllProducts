from playwright.sync_api import sync_playwright
import time

def launch_easemytrip():
    with sync_playwright() as p:
        # Launch browser (headless=False to see the browser window)
        browser = p.chromium.launch(headless=False)
        
        # Create a new browser context
        context = browser.new_context()
        
        # Create a new page
        page = context.new_page()
        
        # Navigate to EaseMyTrip homepage
        print("Navigating to EaseMyTrip...")
        page.goto("https://www.easemytrip.com/")
        
        # Wait for the page to load
        page.wait_for_load_state("networkidle")
        print("Page loaded successfully!")
        
        # Keep the browser open for 10 seconds to view the page
        time.sleep(10)
        
        # Close browser
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()