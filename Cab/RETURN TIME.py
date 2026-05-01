import time
from playwright.sync_api import sync_playwright

def launch_easemytrip():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()

        print("Launching EaseMyTrip homepage...")
        page.goto("https://www.easemytrip.com/")

        page.wait_for_load_state("domcontentloaded")
        print(f"Page Title: {page.title()}")
        print(f"Current URL: {page.url}")

        page.screenshot(path="easemytrip_home.png")
        print("Screenshot saved as easemytrip_home.png")

        # Click on the Cab module
        print("Clicking on Cab module...")
        cab_tab = page.locator('.meuicowidth.cabmenuico')
        cab_tab.wait_for(state="visible", timeout=10000)
        cab_tab.click()
        page.wait_for_load_state("domcontentloaded")
        print(f"Cab Page Title: {page.title()}")
        print(f"Cab Page URL: {page.url}")
        page.screenshot(path="easemytrip_cab.png")
        print("Screenshot saved as easemytrip_cab.png")

        # Click on GetNewCabSection('2')
        print("Clicking on GetNewCabSection('2')...")
        cab_section = page.locator("[onclick=\"GetNewCabSection('2')\"]")
        cab_section.wait_for(state="visible", timeout=10000)
        cab_section.click()
        page.wait_for_load_state("domcontentloaded")
        print(f"Cab Section Page Title: {page.title()}")
        print(f"Cab Section URL: {page.url}")
        page.screenshot(path="easemytrip_cab_section2.png")
        print("Screenshot saved as easemytrip_cab_section2.png")

        # Click on Return Date & Time
        print("Clicking on Return Date & Time...")
        return_calendar = page.locator("#ReturnCalender")
        return_calendar.wait_for(state="visible", timeout=10000)
        return_calendar.click()
        page.wait_for_load_state("domcontentloaded")
        print(f"Return Calendar Page Title: {page.title()}")
        print(f"Return Calendar URL: {page.url}")
        page.screenshot(path="easemytrip_return_calendar.png")
        print("Screenshot saved as easemytrip_return_calendar.png")

        # Click on returntime element before closing
        print("Clicking on returntime...")
        return_time = page.locator("#returntime.f16t")
        return_time.wait_for(state="visible", timeout=10000)
        return_time.click()
        page.screenshot(path="easemytrip_returntime.png")
        print("Screenshot saved as easemytrip_returntime.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
