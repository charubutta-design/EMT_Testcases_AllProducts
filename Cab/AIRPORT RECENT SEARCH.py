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
        
        # Click on the source/from field before search
        print("Clicking on source field...")
        src_field = page.locator(".nwgry.overflw_txt.ftn22.srcShow").first
        src_field.click()
        time.sleep(1)
        
        # Type in source input to trigger autocomplete suggestions
        print("Typing in source field...")
        src_input = page.locator("#a_FromSector_show")
        src_input.press_sequentially("Delhi", delay=100)
        time.sleep(2)
        
        # Click on auto suggestion once visible
        print("Clicking on auto suggestion...")
        auto_sugg = page.locator(".auto_sugg_list:has-text('Indira Gandhi International Airport, Terminal 1')").first
        auto_sugg.wait_for(state="visible", timeout=10000)
        auto_sugg.click()
        time.sleep(1)
        
        # Click on SEARCH button
        print("Clicking on SEARCH button...")
        search_button = page.locator("text=SEARCH").first
        
        # Handle both same-tab navigation and new tab opening
        try:
            with page.context.expect_page(timeout=15000) as new_page_info:
                search_button.click()
                print("Waiting for search results page (new tab)...")
            page = new_page_info.value
            page.wait_for_load_state("domcontentloaded", timeout=60000)
        except Exception:
            print("No new tab opened, waiting for same page navigation...")
            page.wait_for_load_state("domcontentloaded", timeout=60000)
        
        print("Listing page loaded successfully.")
        
        # Click on Cab module
        print("Clicking on Cab module...")
        cab_module = page.locator("._actvrmenu").first
        cab_module.wait_for(state="visible", timeout=10000)
        cab_module.click()
        time.sleep(2)
        
        # Click on Recent Search
        print("Clicking on Recent Search...")
        recent_search = page.locator("#recent_0")
        recent_search.wait_for(state="visible", timeout=10000)
        recent_search.click()
        time.sleep(6)
        
        # Close browser
        browser.close()

if __name__ == "__main__":
    test_easemytrip_cab()
