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

        # Click on element with id="time"
        print("Clicking on element with id='time'...")
        time_field = page.locator('#time')
        time_field.wait_for(state="visible", timeout=10000)
        time_field.click()
        print("Clicked on id='time'")

        # Click on element with class="f16t"
        print("Clicking on element with class='f16t'...")
        f16t_element = page.locator('.f16t')
        f16t_element.wait_for(state="visible", timeout=10000)
        f16t_element.click()
        print("Clicked on class='f16t'")

        page.screenshot(path="easemytrip_cab_time.png")
        print("Screenshot saved as easemytrip_cab_time.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
