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

        # Click on Hourly Rentals (fonro18)
        print("Clicking on Hourly Rentals (fonro18)...")
        fonro18 = page.locator('.fonro18', has_text="Hourly Rentals").first
        fonro18.wait_for(state="attached", timeout=10000)
        fonro18.evaluate("el => el.click()")
        print("Clicked on Hourly Rentals (fonro18).")
        page.screenshot(path="easemytrip_fonro18.png")
        print("Screenshot saved as easemytrip_fonro18.png")

        # Click on Hourly Rentals in the overlay (ovrlyot)
        print("Clicking on Hourly Rentals...")
        hourly_rentals = page.locator('.ovrlyot', has_text="Hourly Rentals")
        hourly_rentals.wait_for(state="visible", timeout=10000)
        hourly_rentals.click()
        print("Clicked on Hourly Rentals.")
        page.screenshot(path="easemytrip_hourly_rentals.png")
        print("Screenshot saved as easemytrip_hourly_rentals.png")

        # Click on Login or Signup
        print("Clicking on Login or Signup...")
        login_signup = page.locator('text=Login or Signup').first
        login_signup.wait_for(state="visible", timeout=10000)
        login_signup.click()
        page.wait_for_load_state("domcontentloaded")
        print("Clicked on Login or Signup.")
        page.screenshot(path="easemytrip_login_signup.png")
        print("Screenshot saved as easemytrip_login_signup.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
