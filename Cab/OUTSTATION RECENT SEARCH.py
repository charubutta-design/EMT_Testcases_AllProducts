from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta

def test_easemytrip():
    with sync_playwright() as p:
        # Loop through dates from today to 10 days ahead
        for days_ahead in range(5, 6):
            print(f"\n{'='*60}")
            print(f"Testing Outstation with date: {days_ahead} days from today")
            print(f"{'='*60}\n")
            
            # Launch browser (headless=False to see the browser)
            browser = p.chromium.launch(headless=False)
            
            # Create a new browser context and page
            context = browser.new_context()
            page = context.new_page()
            
            # Navigate to EaseMyTrip
            page.goto("https://www.easemytrip.com")
            
            # Wait for page to load
            time.sleep(2)
            
            # Click on Cab module
            page.click("text=Cabs")
            
            # Wait for cab page to load
            time.sleep(2)
            
            # Select Outstation/other
            page.click("text=Outstation")
            
            # Wait for outstation page to load
            time.sleep(3)
            
            # Click on 'Enter Pick-up Location'
            page.click("#sourceName")
            print("Clicked on Enter Pick-up Location field")
            
            # Wait for input field to appear and type to trigger suggestions
            time.sleep(1)
            page.keyboard.type("delhi")
            print("Typed 'delhi' to trigger suggestions")
            
            # Wait for suggestions to appear
            time.sleep(3)
            
            # Click on 'delhi darbar' from suggestions - using text match
            page.click("text=delhi darbar")
            print("Selected 'delhi darbar' from suggestions")
            
            # Wait after location selection
            time.sleep(2)
            
            # Click on 'Enter Drop Location'
            page.click("#destinationName")
            print("Clicked on Enter Drop Location field")
            
            # Wait for input field to appear and type to trigger suggestions
            time.sleep(1)
            page.keyboard.type("agra fort")
            print("Typed 'agra fort' to trigger suggestions")
            
            # Wait for suggestions to appear
            time.sleep(3)
            
            # Click on 'Agra Fort' with specific onclick attribute - use force click
            try:
                page.locator("[onclick*=\"ShowStaticAutoSuggForDest('Agra Fort'\"]").click(force=True, timeout=5000)
                print("Selected 'Agra Fort' from suggestions")
            except:
                # Fallback: use JavaScript to click
                page.evaluate("document.querySelector(\"[onclick*='ShowStaticAutoSuggForDest']\").click()")
                print("Selected 'Agra Fort' from suggestions using JavaScript")
            
            # Wait after drop location selection
            time.sleep(2)
            
            # Calculate target date
            pickup_date = datetime.now() + timedelta(days=days_ahead)
            day = pickup_date.day
            month = pickup_date.strftime("%B")  # Full month name like "January"
            year = pickup_date.year
            
            print(f"Selecting date: {day} {month} {year}")
            
            # Click on pick up date & time field - try multiple selectors
            try:
                page.wait_for_selector("input[id*='date'], input[placeholder*='Date'], input[name*='date']", timeout=5000)
                page.click("input[id*='date'], input[placeholder*='Date'], input[name*='date']")
                time.sleep(2)
                
                # Select the date from calendar - try multiple selectors for the date
                date_selectors = [
                    f"//a[text()='{day}']",
                    f"//span[text()='{day}']",
                    f"//td[text()='{day}']",
                    f"//div[text()='{day}']",
                    f"//*[contains(@class, 'day') and text()='{day}']",
                    f"//*[@data-date='{day}']"
                ]
                
                date_clicked = False
                for selector in date_selectors:
                    try:
                        page.click(selector, timeout=3000)
                        print(f"Date {day} selected successfully with selector: {selector}")
                        date_clicked = True
                        break
                    except:
                        continue
                
                if not date_clicked:
                    print(f"Using keyboard navigation to select date...")
                    # Use arrow keys to navigate to target date
                    for i in range(days_ahead):
                        page.keyboard.press("ArrowRight")
                        time.sleep(0.3)
                    page.keyboard.press("Enter")
                    print(f"Date {day} selected using keyboard navigation")
                else:
                    # Wait for time picker to appear
                    time.sleep(2)
                    
                    # Select time - 5 hours
                    print("Attempting to select time...")
                    time_selected = False
                    
                    # Try different time selection methods
                    try:
                        # Method 1: Click on "5 Hr." text
                        page.click("text=5 Hr.", timeout=3000)
                        print(f"Time 5 hours selected via text click")
                        time_selected = True
                    except Exception as e1:
                        print(f"Text click method failed: {e1}")
                        
                        # Method 2: Try typing into hour input field
                        try:
                            page.fill("input[id*='hour'], input[name*='hour'], input[placeholder*='hour']", "05", timeout=3000)
                            print(f"Time 5 hours entered via input field")
                            time_selected = True
                        except Exception as e2:
                            print(f"Input field method failed: {e2}")
                            
                            # Method 3: Try select dropdown
                            try:
                                page.select_option("select[id*='hour'], select[name*='hour'], select[class*='hour']", value="5", timeout=3000)
                                print(f"Time 5 hours selected via dropdown")
                                time_selected = True
                            except Exception as e3:
                                print(f"Dropdown method failed: {e3}")
                                page.screenshot(path="time_debug.png")
                    
                    if not time_selected:
                        print("Could not select time with any method, continuing anyway...")
                    else:
                        # Select minutes - 00 Min.
                        time.sleep(1)
                        try:
                            page.click("text=00 Min.", timeout=3000)
                            print("00 Min. selected successfully")
                            
                            # Click Done button
                            time.sleep(1)
                            done_clicked = False
                            done_selectors = [
                                ".done_d",
                                "//button[@class='done_d']",
                                "//*[@class='done_d']",
                                "button:has-text('Done')",
                                "//button[text()='Done']",
                                "//a[text()='Done']"
                            ]
                            
                            for selector in done_selectors:
                                try:
                                    page.click(selector, timeout=2000)
                                    print(f"Done button clicked with selector: {selector}")
                                    done_clicked = True
                                    break
                                except:
                                    continue
                            
                            if not done_clicked:
                                print("Could not click Done button")
                                page.screenshot(path="done_debug.png")
                        except Exception as e:
                            print(f"Error: {e}")
                
            except Exception as e:
                print(f"Error selecting date: {e}")
                # Take a screenshot to debug
                page.screenshot(path="debug.png")
            
            # Wait to see the selected date and time
            time.sleep(3)
            
            # Click on Search button
            try:
                page.click(".srch-btn-c", timeout=5000)
                print("Search button clicked successfully")
            except Exception as e:
                print(f"Could not click Search button: {e}")
                page.screenshot(path="search_debug.png")
            
            # Wait to see search results
            time.sleep(5)

            print(f"Listing page loaded for {pickup_date.strftime('%d %B %Y')}!")

            # Click on Cab module
            try:
                page.click(".meuicowidth.cabmenuico", timeout=5000)
                print("Cab module clicked successfully")
            except Exception as e:
                print(f"Could not click Cab module: {e}")
                page.screenshot(path="cab_module_debug.png")

            time.sleep(2)

            # Click on Recent Search
            try:
                page.click("#recent_0", timeout=5000)
                print("Recent Search clicked successfully")
            except Exception as e:
                print(f"Could not click Recent Search: {e}")
                page.screenshot(path="recent_search_debug.png")

            time.sleep(6)

            # Close browser
            context.close()
            browser.close()

            print(f"\nCompleted test for day {days_ahead}. Moving to next date...\n")

if __name__ == "__main__":
    test_easemytrip()
