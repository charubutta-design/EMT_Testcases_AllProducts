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

        # Click on 'Deal of the Day' banner
        print("Clicking on 'Deal of the Day' banner...")
        deal_banner = page.locator('.ovrlyot').filter(has_text="Deal of the Day").first
        deal_banner.wait_for(state="visible", timeout=10000)
        deal_banner.click()
        time.sleep(4)
        page.wait_for_load_state("domcontentloaded")
        print(f"Deal of the Day Page Title: {page.title()}")
        print(f"Deal of the Day Page URL: {page.url}")
        page.screenshot(path="easemytrip_deal_of_the_day.png")
        print("Screenshot saved as easemytrip_deal_of_the_day.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
