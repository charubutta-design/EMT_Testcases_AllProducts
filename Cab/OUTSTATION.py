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
            
            # Click on Book Now button
            try:
                page.click(".slct_btn", timeout=5000)
                print("Book Now button clicked successfully")
            except Exception as e:
                print(f"Could not click Book Now button: {e}")
                page.screenshot(path="booknow_debug.png")
            
            # Wait after booking
            time.sleep(3)
            
            # Click on heritage contribution option
            try:
                # Click on the radio button with class radio_label_plant
                page.click(".radio_label_plant", timeout=5000)
                print("Heritage contribution radio button (₹10) clicked successfully")
            except Exception as e:
                print(f"Could not click heritage contribution radio: {e}")
                page.screenshot(path="heritage_debug.png")
            
            # Wait after selection
            time.sleep(3)
            
            # Scroll and click on Enter First Name field under Travellers Details
            try:
                # Wait for the field to be visible
                page.wait_for_selector("#txtfname", state="visible", timeout=10000)
                
                # Scroll to the element
                page.locator("#txtfname").scroll_into_view_if_needed()
                time.sleep(1)
                
                # Click on the field
                page.click("#txtfname", force=True)
                print("First Name field clicked successfully")
                
                # Enter 'Test' in the field
                page.fill("#txtfname", "Test")
                print("Entered 'Test' in First Name field")
            except Exception as e:
                print(f"Could not click/fill First Name field: {e}")
                page.screenshot(path="firstname_debug.png")
            
            # Wait after clicking
            time.sleep(1)
            
            # Click on Last Name field
            try:
                page.wait_for_selector("#txtlname", state="visible", timeout=10000)
                page.locator("#txtlname").scroll_into_view_if_needed()
                time.sleep(1)
                page.click("#txtlname", force=True)
                print("Last Name field clicked successfully")
                
                # Enter 'Test' in the field
                page.fill("#txtlname", "Test")
                print("Entered 'Test' in Last Name field")
            except Exception as e:
                print(f"Could not click/fill Last Name field: {e}")
                page.screenshot(path="lastname_debug.png")
            
            # Wait after clicking
            time.sleep(1)
            
            # Click on Email field
            try:
                page.wait_for_selector("#txtemail", state="visible", timeout=10000)
                page.locator("#txtemail").scroll_into_view_if_needed()
                time.sleep(1)
                page.click("#txtemail", force=True)
                print("Email field clicked successfully")
                
                # Enter email ID
                page.fill("#txtemail", "megha.goswami@easemyytrip.com")
                print("Entered 'megha.goswami@easemyytrip.com' in Email field")
            except Exception as e:
                print(f"Could not click/fill Email field: {e}")
                page.screenshot(path="email_debug.png")
            
            # Wait after clicking
            time.sleep(1)
            
            # Click on Phone field
            try:
                phone_selectors = [
                    "#txtmbl",
                    "#txtmobile",
                    "#mobile",
                    "input[name*='mobile']",
                    "input[placeholder*='Phone']",
                    "input[placeholder*='Mobile']"
                ]
                
                phone_clicked = False
                for selector in phone_selectors:
                    try:
                        page.wait_for_selector(selector, state="visible", timeout=3000)
                        page.locator(selector).scroll_into_view_if_needed()
                        time.sleep(1)
                        page.click(selector, force=True)
                        print(f"Phone field clicked with selector: {selector}")
                        
                        # Enter phone number
                        page.fill(selector, "9999999999")
                        print("Entered '9999999999' in Phone field")
                        phone_clicked = True
                        break
                    except:
                        continue
                
                if not phone_clicked:
                    print("Could not click Phone field")
                    page.screenshot(path="phone_debug.png")
            except Exception as e:
                print(f"Error: {e}")
            
            # Wait after clicking
            time.sleep(1)
            
            # Click on Enter Exact Pickup Location field
            try:
                page.wait_for_selector("#txtpadd", state="visible", timeout=10000)
                page.locator("#txtpadd").scroll_into_view_if_needed()
                time.sleep(1)
                page.click("#txtpadd", force=True)
                print("Pickup Location field clicked successfully")
                
                # Enter 'ABC' in the field
                page.fill("#txtpadd", "ABC")
                print("Entered 'ABC' in Pickup Location field")
            except Exception as e:
                print(f"Could not click/fill Pickup Location field: {e}")
                page.screenshot(path="pickup_debug.png")
            
            # Wait after clicking
            time.sleep(1)
            
            # Click on Enter Exact Drop Location field
            try:
                page.wait_for_selector("#txtdadd", state="visible", timeout=10000)
                page.locator("#txtdadd").scroll_into_view_if_needed()
                time.sleep(1)
                page.click("#txtdadd", force=True)
                print("Drop Location field clicked successfully")
                
                # Enter 'ABC' in the field
                page.fill("#txtdadd", "ABC")
                print("Entered 'ABC' in Drop Location field")
            except Exception as e:
                print(f"Could not click/fill Drop Location field: {e}")
                page.screenshot(path="drop_debug.png")
            
            # Wait after clicking
            time.sleep(1)
            
            # Click on Continue to payment button
            try:
                # Wait a bit more for the button to be ready
                time.sleep(3)
                
                # Scroll to bottom of page first
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                
                # Try clicking with JavaScript
                try:
                    page.evaluate("document.querySelector('button.cnt-btn').click()")
                    print("Continue to payment button clicked with JavaScript")
                except:
                    # Fallback to force click
                    page.locator("button.cnt-btn").first.click(force=True, timeout=5000)
                    print("Continue to payment button clicked with force")
            except Exception as e:
                print(f"Could not click Continue to payment button: {e}")
                page.screenshot(path="payment_debug.png")
            
            # Wait after clicking
            time.sleep(5)
            
            # Click on payment section first
            try:
                time.sleep(3)
                
                # Click on 'Choose Mobikwik, Payzapp, PhonePe or Amazon' section to expand
                section_selectors = [
                    "text=Choose Mobikwik, Payzapp, PhonePe or Amazon",
                    "//*[contains(text(), 'Choose Mobikwik')]",
                    "//*[contains(text(), 'Payzapp')]"
                ]
                
                section_clicked = False
                for selector in section_selectors:
                    try:
                        page.click(selector, timeout=3000)
                        print(f"Payment section clicked: {selector}")
                        section_clicked = True
                        break
                    except:
                        continue
                
                if not section_clicked:
                    print("Could not click payment section")
                
                # Wait for options to appear
                time.sleep(2)
                
            except Exception as e:
                print(f"Error clicking payment section: {e}")
            
            # Click on payment method - Bajaj Pay
            try:
                payment_options = [
                    ".ftn14.ng-binding:has-text('Bajaj Pay')",
                    "//span[@class='ftn14 ng-binding' and contains(text(), 'Bajaj Pay')]",
                    "text=Bajaj Pay",
                    "//label[contains(text(), 'Bajaj Pay')]"
                ]
                
                payment_selected = False
                for option in payment_options:
                    try:
                        page.click(option, timeout=3000)
                        print(f"Bajaj Pay selected: {option}")
                        payment_selected = True
                        break
                    except:
                        continue
                
                if not payment_selected:
                    print("Could not select Bajaj Pay option")
                    page.screenshot(path="bajaj_pay_debug.png")
            except Exception as e:
                print(f"Error selecting Bajaj Pay: {e}")
            
            # Wait after payment selection
            time.sleep(3)
            
            # Click on Make Payment button
            try:
                make_payment_selectors = [
                    ".mk-pym4",
                    "button.mk-pym4",
                    "//button[@class='mk-pym4']",
                    "//*[contains(@class, 'mk-pym4')]"
                ]
                
                payment_clicked = False
                for selector in make_payment_selectors:
                    try:
                        # Scroll to button first
                        if selector.startswith(".") or selector.startswith("button"):
                            page.locator(selector).scroll_into_view_if_needed()
                            time.sleep(1)
                        
                        page.click(selector, timeout=3000, force=True)
                        print(f"Make Payment button clicked: {selector}")
                        payment_clicked = True
                        break
                    except:
                        continue
                
                if not payment_clicked:
                    print("Could not click Make Payment button")
                    page.screenshot(path="make_payment_debug.png")
            except Exception as e:
                print(f"Error clicking Make Payment: {e}")
            
            # Wait after making payment
            time.sleep(5)
            
            # Take screenshot and save to specified path with date info
            try:
                screenshot_filename = f"outstation_payment_page_day_{days_ahead}.png"
                screenshot_path = rf"C:\Users\megha.goswami\Cab_GIT_TC\Screenshot\{screenshot_filename}"
                page.screenshot(path=screenshot_path)
                print(f"Screenshot saved to: {screenshot_path}")
            except Exception as e:
                print(f"Error saving screenshot: {e}")
            
            print(f"Successfully completed outstation cab booking for {pickup_date.strftime('%d %B %Y')}!")
            
            # Close browser
            context.close()
            browser.close()
            
            print(f"\nCompleted test for day {days_ahead}. Moving to next date...\n")

if __name__ == "__main__":
    test_easemytrip()
