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

        # Click on ShowAutoSuggForDest (Outstation destination input)
        print("Clicking on ShowAutoSuggForDest()...")
        dest_input = page.locator("[onclick='ShowAutoSuggForDest()']")
        dest_input.wait_for(state="visible", timeout=10000)
        dest_input.click()
        page.wait_for_load_state("domcontentloaded")
        print(f"ShowAutoSuggForDest Page Title: {page.title()}")
        print(f"ShowAutoSuggForDest URL: {page.url}")
        page.screenshot(path="easemytrip_dest_autosugg.png")
        print("Screenshot saved as easemytrip_dest_autosugg.png")

        print("Closing browser in 1 second...")
        time.sleep(1)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    launch_easemytrip()
