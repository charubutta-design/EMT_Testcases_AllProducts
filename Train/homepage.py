from playwright.sync_api import sync_playwright


def launch_easemytrip_in_chrome() -> None:

	with sync_playwright() as p:
		browser = p.chromium.launch(channel="chrome", headless=False)
		page = browser.new_page()
		page.goto("https://www.easemytrip.com/")
		page.wait_for_timeout(5000)
		browser.close()


if __name__ == "__main__":
	launch_easemytrip_in_chrome()

