from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta

def test_easemytrip_hourly_cab():
    """Test case for Hourly cab booking on EaseMyTrip"""
    with sync_playwright() as p:
        # Select date 5 days ahead from current date
        for days_ahead in range(5, 6):
            print(f"\n{'='*60}")
            print(f"Testing Hourly with date: {days_ahead} days from today")
            print(f"{'='*60}\n")
            
            # Launch browser
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            # Open easemytrip.com
            print("Opening easemytrip.com...")
            page.goto("https://www.easemytrip.com", timeout=60000)
            page.wait_for_load_state("domcontentloaded", timeout=60000)
            time.sleep(2)
            
            # Click on cab module
            print("Clicking on cab module...")
            cab_module = page.locator("text=Cabs").first
            cab_module.click(timeout=10000)
            time.sleep(3)
            
            # Click on Hourly option
            print("Clicking on Hourly option...")
            hourly_option = page.locator("text=Hourly").first
            hourly_option.click()
            time.sleep(3)
            
            # Fill pickup location with Delhi
            print("Filling 'Enter Pick-up Location' (From field) with Delhi...")
            try:
                # First click on the sourceName div to activate the input field
                print("Clicking on From field (pickup location div)...")
                source_name_div = page.locator("#sourceName")
                source_name_div.wait_for(state="visible", timeout=5000)
                source_name_div.click()
                time.sleep(1)
                
                # Now the actual input field should be visible
                print("Typing 'Delhi' in From field...")
                pickup_input = page.locator("#a_FromSector_show")
                pickup_input.wait_for(state="visible", timeout=5000)
                pickup_input.fill("Delhi")
                time.sleep(2)
                
                print("Waiting for dropdown suggestions to appear...")
                # Wait for dropdown to appear
                page.wait_for_selector(".auto_sugg_add", timeout=5000)
                time.sleep(1)
                
                print("Clicking on 'delhi' option with class='auto_sugg_add'...")
                # Click on the specific option that contains "delhi"
                selected = False
                selectors_to_try = [
                    ".auto_sugg_add:has-text('delhi')",
                    ".auto_sugg_add:has-text('Delhi')",
                    ".auto_sugg_add:text-is('delhi')",
                    ".auto_sugg_add:text-is('Delhi')",
                    ".auto_sugg_add"
                ]
                
                for selector in selectors_to_try:
                    try:
                        print(f"Trying selector: {selector}")
                        delhi_option = page.locator(selector).first
                        delhi_option.click(timeout=3000)
                        selected = True
                        print(f"Successfully clicked 'delhi' with selector: {selector}")
                        break
                    except Exception as e:
                        print(f"Selector {selector} failed: {str(e)[:100]}")
                        continue
                
                if selected:
                    time.sleep(2)
                    print("Successfully selected Delhi from dropdown")
                else:
                    print("Could not click dropdown option")
            except Exception as e:
                print(f"Error filling From field (pickup location): {e}")
                print("Continuing with the rest of the flow...")
            
            time.sleep(1)
            
            # Click on Pick-Up Date & Time
            print("Clicking on Pick-Up Date & Time...")
            pickup_calendar = page.locator("#pickCalender")
            pickup_calendar.click()
            time.sleep(3)
            
            # Calculate target date
            target_date = datetime.now() + timedelta(days=days_ahead)
            target_day = str(target_date.day)
            
            print(f"Selecting date: {target_date.strftime('%d %B %Y')}")
            
            # Try clicking the date - wait for calendar to be visible
            try:
                # Wait for calendar to appear
                page.wait_for_selector(".calendar, .datepicker, [class*='calendar']", timeout=5000)
                time.sleep(1)
                
                # Try different selectors for the date
                date_clicked = False
                selectors_to_try = [
                    f"a:text-is('{target_day}')",
                    f"a:has-text('{target_day}'):not(.disabled)",
                    f".day:has-text('{target_day}'):not(.disabled)",
                    f"td:has-text('{target_day}'):not(.disabled)"
                ]
                
                for selector in selectors_to_try:
                    try:
                        print(f"Trying selector: {selector}")
                        date_elements = page.locator(selector)
                        count = date_elements.count()
                        if count > 0:
                            # Click the last occurrence (future date)
                            date_elements.last.click(timeout=3000)
                            date_clicked = True
                            print(f"Date selected with selector: {selector}")
                            break
                    except Exception as e:
                        print(f"Selector {selector} failed: {e}")
                        continue
                
                if not date_clicked:
                    print("Using keyboard navigation to select date...")
                    # Use arrow keys to navigate to target date
                    for i in range(days_ahead):
                        page.keyboard.press("ArrowRight")
                        time.sleep(0.3)
                    page.keyboard.press("Enter")
            except Exception as e:
                print(f"Date selection error: {e}")
            
            time.sleep(2)
            
            # Click on 10 Hr option for hourly booking
            print("Clicking on 10 Hr option...")
            ten_hr = page.locator("text=10 Hr").first
            ten_hr.click()
            time.sleep(1)
            
            # Click on 30 Min option
            print("Clicking on 30 Min option...")
            thirty_min = page.locator("text=30 Min").first
            thirty_min.click()
            time.sleep(1)
            
            # Click on Done button
            print("Clicking on Done button...")
            done_button = page.locator(".done_d[onclick='Done(event)']")
            done_button.click()
            time.sleep(2)
            
            # Click on SEARCH button
            print("Clicking on SEARCH button...")
            search_button = page.locator("text=SEARCH").first
            search_button.click()
            
            # Wait for search results page to load
            print("Waiting for search results...")
            page.wait_for_load_state("domcontentloaded", timeout=60000)
            time.sleep(15)
            
            # Scroll down to load cabs
            page.evaluate("window.scrollBy(0, 500)")
            time.sleep(5)
            
            # Click on first BOOK NOW button
            print("Clicking on BOOK NOW button...")
            book_now = page.locator(".slct_btn").first
            book_now.wait_for(state="visible", timeout=20000)
            book_now.click()
            time.sleep(5)
            
            # Fill traveler details
            print("Entering First Name...")
            first_name = page.locator("#txtfname")
            first_name.click()
            first_name.fill("Test")
            time.sleep(1)
            
            print("Entering Last Name...")
            last_name = page.locator("#txtlname")
            last_name.click()
            last_name.fill("User")
            time.sleep(1)
            
            print("Entering Email...")
            email = page.locator("#txtemail")
            email.click()
            email.fill("test.user@easemytrip.com")
            time.sleep(1)
            
            print("Entering Mobile Number...")
            mobile = page.locator("#txtmbl")
            mobile.click()
            mobile.fill("9876543210")
            time.sleep(1)
            
            print("Entering Pickup Location...")
            try:
                pickup_location = page.locator("#txtpadd")
                pickup_location.wait_for(state="visible", timeout=5000)
                pickup_location.scroll_into_view_if_needed()
                pickup_location.click()
                pickup_location.fill("Connaught Place, Delhi")
                time.sleep(1)
            except Exception as e:
                print(f"Pickup location field error: {e}")
            
            print("Entering Drop Location...")
            try:
                drop_location = page.locator("#txtdadd")
                drop_location.wait_for(state="visible", timeout=5000)
                drop_location.scroll_into_view_if_needed()
                drop_location.click()
                drop_location.fill("Connaught Place, Delhi")
                time.sleep(2)
            except Exception as e:
                print(f"Drop location field error: {e}")
            
            # Scroll down to Continue to Payment button
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(2)
            
            # Click on Continue to Payment button
            print("Clicking on Continue to Payment button...")
            try:
                continue_payment = page.locator(".cnt-btn").first
                page.evaluate("(element) => element.click()", continue_payment.element_handle())
            except:
                continue_payment = page.locator("button:has-text('Continue to Payment')").first
                continue_payment.click(force=True)
            
            # Wait for payment page to load
            print("Waiting for payment page to load...")
            time.sleep(8)
            
            # Take screenshot
            page.screenshot(path="payment_page_hourly.png")
            
            # Click on payment wallet option
            print("Clicking on payment wallet option...")
            try:
                payment_option = page.locator(".pymtsbtxt.ng-binding:has-text('Mobikwik')").first
                payment_option.wait_for(state="visible", timeout=10000)
                payment_option.click()
            except:
                payment_option = page.locator("text=Choose Mobikwik, Payzapp, PhonePe or Amazon").first
                payment_option.click(force=True)
            
            time.sleep(2)
            
            # Click on Bajaj Pay radio button
            print("Clicking on Bajaj Pay...")
            bajaj_pay = page.locator(".ftn14.ng-binding:has-text('Bajaj Pay')").first
            bajaj_pay.click()
            time.sleep(2)
            
            # Click on Make Payment button
            print("Clicking on Make Payment button...")
            make_payment = page.locator(".mk-pym4").first
            make_payment.scroll_into_view_if_needed()
            time.sleep(1)
            make_payment.click()
            time.sleep(5)
            
            # Take final screenshot with date info
            print("Taking final screenshot...")
            screenshot_filename = f"hourly_final_page_day_{days_ahead}.png"
            screenshot_path = rf"C:\Users\megha.goswami\Cab_GIT_TC\Screenshot\{screenshot_filename}"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved at: {screenshot_path}")
            
            time.sleep(3)
            print(f"Successfully completed hourly cab booking for {target_date.strftime('%d %B %Y')}!")
            
            # Close browser
            browser.close()
            
            print(f"\nCompleted test for day {days_ahead}. Moving to next date...\n")

if __name__ == "__main__":
    test_easemytrip_hourly_cab()
