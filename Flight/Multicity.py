from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as p:
        # Launch browser with custom args for maximized window
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context without default viewport to allow full screen
        context = browser.new_context(no_viewport=True)
        
        page = context.new_page()
        
        # Navigate to EaseMyTrip
        page.goto("https://www.easemytrip.com")
        
        # Wait for page load
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # Multiple selector options to try
        selectors = [
            "text=Multicity",
            "label:has-text('Multicity')",
            "//label[contains(text(), 'Multicity')]",
        ]
        
        clicked = False
        for selector in selectors:
            try:
                page.click(selector, timeout=5000)
                print(f"✓ Successfully clicked Multicity using: {selector}")
                clicked = True
                break
            except Exception as e:
                print(f"✗ Failed with selector {selector}")
                continue
        
        if not clicked:
            print("Failed to click Multicity with all selectors")
        
        # Wait to observe the result
        time.sleep(5)
        
        browser.close()

if __name__ == "__main__":
    main()