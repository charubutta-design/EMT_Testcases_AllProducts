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

        # Click on Outstation tab
        print("Clicking on Outstation tab...")
        outstation_tab = page.locator("[onclick=\"GetNewCabSection('2')\"]")
        outstation_tab.wait_for(state="visible", timeout=10000)
        outstation_tab.click()
        page.wait_for_load_state("domcontentloaded")
        print(f"Outstation Page Title: {page.title()}")
        print(f"Outstation URL: {page.url}")
        page.screenshot(path="easemytrip_outstation.png")
        print("Screenshot saved as easemytrip_outstation.png")

        # Click on Pick Date Calendar (class="in-bx-d showPickCalender", id="pickCalender")
        print("Clicking on Pick Date Calendar...")
        pick_calendar = page.locator("#pickCalender")
        pick_calendar.wait_for(state="visible", timeout=10000)
        pick_calendar.click()
        page.wait_for_timeout(1000)
        page.screenshot(path="easemytrip_pick_calendar.png")
        print("Screenshot saved as easemytrip_pick_calendar.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
