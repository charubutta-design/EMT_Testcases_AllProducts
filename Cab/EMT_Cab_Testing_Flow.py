from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta

def test_easemytrip_cab():
    with sync_playwright() as p:
        # Set date to 5 days forward from current date
        days_ahead = 5
        print(f"\n{'='*60}")
        print(f"Testing with date: {days_ahead} days from today")
        print(f"{'='*60}\n")
        
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Open easemytrip.com
        print("Opening easemytrip.com...")
        page.goto("https://www.easemytrip.com", timeout=60000)
        page.wait_for_load_state("domcontentloaded", timeout=60000)
        
        # Wait a bit for page to stabilize
        time.sleep(2)
        
        # Click on cab module
        print("Clicking on cab module...")
        cab_module = page.locator("text=Cabs").first
        cab_module.click(timeout=10000)
        
        # Wait for cab page to load
        time.sleep(3)
        
        # Click on 'To' field using the correct class
        print("Clicking on 'To' field...")
        to_field = page.locator(".f12.gry.destShow").first
        to_field.click()
        
        # Type 'Agra Fort' in the input field
        print("Typing 'Agra Fort'...")
        to_input = page.locator("#a_ToSector_show")
        to_input.fill("Agra Fort")
        time.sleep(2)
        
        # Click on 'near taj mahal' option
        print("Clicking on 'near taj mahal' from dropdown...")
        near_taj_mahal = page.locator("#citiesWhenKeyIsLessForDest >> text=near taj mahal")
        near_taj_mahal.click(force=True)
        
        # Wait a bit after selection
        time.sleep(2)
        
        # Click on Pick-Up Date & Time
        print("Clicking on Pick-Up Date & Time...")
        pickup_calendar = page.locator("#pickCalender")
        pickup_calendar.click()
        
        # Wait for calendar to appear
        time.sleep(3)
        
        # Calculate target date
        target_date = datetime.now() + timedelta(days=days_ahead)
        target_day = str(target_date.day)
        
        print(f"Selecting date: {target_date.strftime('%d %B %Y')}")
        
        # Try clicking using different selector - typically calendar dates are in span/a tags
        # Try multiple possible selectors
        selectors_to_try = [
            f"a:has-text('{target_day}')",
            f"span:text('{target_day}')",
            f"div:text-is('{target_day}')",
            f"[data-date='{target_day}']"
        ]
        
        clicked = False
        for selector in selectors_to_try:
            try:
                print(f"Trying selector: {selector}")
                date_element = page.locator(selector).first
                date_element.click(timeout=5000)
                clicked = True
                break
            except:
                continue
        
        if not clicked:
            print("Using keyboard navigation to select date...")
            # Use arrow keys to navigate to target date
            for i in range(days_ahead):
                page.keyboard.press("ArrowRight")
                time.sleep(0.3)
            page.keyboard.press("Enter")
        
        # Wait after date selection
        time.sleep(2)
        
        # Click on 6 Hr option
        print("Clicking on 6 Hr option...")
        six_hr = page.locator("text=6 Hr").first
        six_hr.click()
        
        # Wait after hour selection
        time.sleep(1)
        
        # Click on 00 Min option
        print("Clicking on 00 Min option...")
        zero_min = page.locator("text=00 Min").first
        zero_min.click()
        
        # Wait after minute selection
        time.sleep(1)
        
        # Click on Done button using the correct class and onclick attribute
        print("Clicking on Done button...")
        done_button = page.locator(".done_d[onclick='Done(event)']")
        done_button.click()
        
        # Wait after Done button
        time.sleep(2)
        
        # Click on SEARCH button
        print("Clicking on SEARCH button...")
        search_button = page.locator("text=SEARCH").first
        search_button.click()
        
        # Wait for search results page to load completely
        print("Waiting for search results...")
        page.wait_for_load_state("domcontentloaded", timeout=60000)
        time.sleep(15)
        
        # Scroll down to load cabs
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(5)
        
        # Click on first BOOK NOW button using correct class
        print("Clicking on BOOK NOW button...")
        book_now = page.locator(".slct_btn").first
        book_now.wait_for(state="visible", timeout=20000)
        book_now.click()
        
        # Wait for booking page to load
        time.sleep(5)
        
        # Click on First Name field and enter 'Test'
        print("Entering First Name...")
        first_name = page.locator("#txtfname")
        first_name.click()
        first_name.fill("Test")
        
        # Wait a bit
        time.sleep(1)
        
        # Click on Last Name field and enter 'Test'
        print("Entering Last Name...")
        last_name = page.locator("#txtlname")
        last_name.click()
        last_name.fill("Test")
        
        # Wait a bit
        time.sleep(1)
        
        # Click on Email field and enter email address
        print("Entering Email...")
        email = page.locator("#txtemail")
        email.click()
        email.fill("megha.goswami@easemytrip.com")
        
        # Wait a bit
        time.sleep(1)
        
        # Click on Mobile number field and enter mobile number
        print("Entering Mobile Number...")
        mobile = page.locator("#txtmbl")
        mobile.click()
        mobile.fill("9999999999")
        
        # Wait a bit
        time.sleep(1)
        
        # Click on Drop location field and enter location
        print("Entering Drop Location...")
        drop_location = page.locator("#txtdadd")
        drop_location.click()
        drop_location.fill("Agra Bus Stand")
        
        # Wait a bit
        time.sleep(1)
        
        # Click on Flight No. field and enter flight number
        print("Entering Flight Number...")
        flight_no = page.locator("#txtflightno")
        flight_no.click()
        flight_no.fill("ABC123")
        
        # Wait a bit
        time.sleep(2)
        
        # Take screenshot before Continue to Payment
        page.screenshot(path="before_continue_payment.png")
        
        # Scroll down to see Continue to Payment button
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(2)
        
        # Click on Continue to Payment button using JavaScript
        print("Clicking on Continue to Payment button...")
        try:
            continue_payment = page.locator(".cnt-btn").first
            page.evaluate("(element) => element.click()", continue_payment.element_handle())
        except:
            # Try clicking with text
            continue_payment = page.locator("button:has-text('Continue to Payment')").first
            continue_payment.click(force=True)
        
        # Wait for payment page to load completely
        print("Waiting for payment page to load...")
        time.sleep(8)
        
        # Take screenshot to debug
        page.screenshot(path="payment_page.png")
        
        # Click on Choose Mobikwik, Payzapp, PhonePe or Amazon option
        print("Clicking on payment wallet option...")
        try:
            payment_option = page.locator(".pymtsbtxt.ng-binding:has-text('Mobikwik')").first
            payment_option.wait_for(state="visible", timeout=10000)
            payment_option.click()
        except:
            # Try alternative selector
            payment_option = page.locator("text=Choose Mobikwik, Payzapp, PhonePe or Amazon").first
            payment_option.click(force=True)
        
        # Wait for payment options to expand
        time.sleep(2)
        
        # Click on Bajaj Pay radio button
        print("Clicking on Bajaj Pay...")
        bajaj_pay = page.locator(".ftn14.ng-binding:has-text('Bajaj Pay')").first
        bajaj_pay.click()
        
        # Wait for option to be selected
        time.sleep(2)
        
        # Click on Make Payment button
        print("Clicking on Make Payment button...")
        make_payment = page.locator(".mk-pym4").first
        make_payment.scroll_into_view_if_needed()
        time.sleep(1)
        make_payment.click()
        
        # Wait for payment gateway to load
        time.sleep(5)
        
        # Take screenshot and save in specified path with date info
        print("Taking screenshot...")
        screenshot_filename = f"final_page_day_{days_ahead}.png"
        screenshot_path = rf"C:\Users\megha.goswami\Cab_GIT_TC\Screenshot\{screenshot_filename}"
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved at: {screenshot_path}")
        
        # Wait to see the result
        time.sleep(3)
            
        print(f"Successfully completed booking for {target_date.strftime('%d %B %Y')}!")
        
        # Close browser
        browser.close()
        
        print(f"\nCompleted test for day {days_ahead}.")

if __name__ == "__main__":
    test_easemytrip_cab()
