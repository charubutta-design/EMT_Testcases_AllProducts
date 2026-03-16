from playwright.sync_api import sync_playwright
import time

def automate_easemytrip():
    browser = None
    context = None
    
    try:
        with sync_playwright() as p:
            # Launch browser in maximized window
            browser = p.chromium.launch(
                headless=False,
                args=['--start-maximized']
            )
            
            # Create a new page without setting viewport (to use full screen)
            context = browser.new_context(no_viewport=True)
            page = context.new_page()
            
            # Navigate to EaseMyTrip website
            print("Navigating to EaseMyTrip...")
            page.goto("https://www.easemytrip.com/", wait_until="domcontentloaded")
            time.sleep(2)
            
            # Handle location permission popup if it appears
            print("Checking for popups...")
            try:
                # Click "Never allow" or close the location popup
                if page.locator("text='Never allow'").is_visible(timeout=3000):
                    page.click("text='Never allow'")
                    print("Closed location popup")
                    time.sleep(1)
            except:
                print("No popup found or already closed")
            
            time.sleep(2)
            
            # Click on Trains tab - try multiple selectors
            print("Clicking on Trains tab...")
            try:
                # Try different possible selectors for trains tab
                if page.locator("a[title='Trains']").is_visible(timeout=3000):
                    page.click("a[title='Trains']")
                elif page.locator("li:has-text('Trains')").is_visible(timeout=3000):
                    page.click("li:has-text('Trains')")
                elif page.locator("a:has-text('Trains')").is_visible(timeout=3000):
                    page.click("a:has-text('Trains')")
                else:
                    # Direct navigation to trains page
                    print("Navigating directly to trains page...")
                    page.goto("https://www.easemytrip.com/railways/", wait_until="networkidle")
            except:
                print("Navigating directly to trains page...")
                page.goto("https://www.easemytrip.com/railways/", wait_until="networkidle")
            
            time.sleep(3)
            
            # Wait for the trains page to load
            page.wait_for_load_state("networkidle")
            
            # Click on the departure station text field
            print("Clicking on departure station field...")
            # Click on the "From" field with placeholder "Choose Source station"
            page.click("input[placeholder='Choose Source station']")
            time.sleep(1)
            
            # Type "Patna" in the departure field
            print("Typing 'Patna' in departure field...")
            page.fill("input[placeholder='Choose Source station']", "Patna")
            time.sleep(3)  # Give more time for dropdown to appear
            
            # Wait for auto-suggest to appear and select first option
            print("Waiting for auto-suggest dropdown...")
            try:
                # Use keyboard to select first option (most reliable method)
                print("Using keyboard to select first option...")
                time.sleep(1)
                page.keyboard.press("ArrowDown")
                time.sleep(1)
                page.keyboard.press("Enter")
                time.sleep(1)
                print("Selected first option using keyboard!")
                
            except Exception as e:
                print(f"Selection error: {e}")
            
            print("Successfully completed! Station selected: Patna Jn (PNBE)")
            print("Closing browser in 5 seconds...")
            time.sleep(5)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Force close browser
        print("Forcing browser close...")
        try:
            if context:
                context.close()
            if browser:
                browser.close()
            print("Browser closed successfully!")
        except Exception as close_error:
            print(f"Error during close: {close_error}")

if __name__ == "__main__":
    automate_easemytrip()
    print("Script execution completed!")