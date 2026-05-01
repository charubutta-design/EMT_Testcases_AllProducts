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

        # Click on the pick date calendar trigger
        print("Clicking on showPickCalender...")
        pick_cal_trigger = page.locator('.in-bx-d.showPickCalender')
        pick_cal_trigger.wait_for(state="visible", timeout=10000)
        pick_cal_trigger.click()

        # Wait for the calendar to appear
        print("Waiting for pickCalender to appear...")
        pick_calendar = page.locator('#pickCalender')
        pick_calendar.wait_for(state="visible", timeout=10000)
        print("pickCalender is visible.")
        page.screenshot(path="easemytrip_cab_calendar.png")
        print("Screenshot saved as easemytrip_cab_calendar.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
