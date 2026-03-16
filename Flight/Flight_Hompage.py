from playwright.sync_api import sync_playwright
import time

def navigate_to_flights():
    with sync_playwright() as p:
        # Launch browser with maximized window
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context with no viewport (uses full screen)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        # Navigate to EaseMyTrip website
        print("Navigating to EaseMyTrip...")
        page.goto("https://www.easemytrip.com/")
        
        # Wait for page to load
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # Handle location permission popup - click "Never allow" or close
        try:
            print("Handling location popup...")
            never_allow_btn = page.locator('text="Never allow"').first
            if never_allow_btn.is_visible(timeout=2000):
                never_allow_btn.click()
                print("Closed location popup")
        except:
            print("No location popup found or already closed")
        
        # Wait a moment after closing popup
        time.sleep(1)
        
        # Ensure we're on the Flights tab (it should be selected by default)
        try:
            # Look for the Flights tab in the navigation
            flights_tab = page.locator('text="Flights"').first
            if flights_tab.is_visible():
                flights_tab.click()
                print("Clicked on Flights tab")
                time.sleep(2)
        except:
            print("Flights section already active")
        
        print("Successfully navigated to Flights homepage!")
        time.sleep(2)
        
        print("Script completed. Browser will remain open.")
        print("Press Ctrl+C to close the browser.")
        
        # Keep browser open until user closes it
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing browser...")
            browser.close()

if __name__ == "__main__":
    navigate_to_flights()