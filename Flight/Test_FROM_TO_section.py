from playwright.sync_api import sync_playwright
import time

def automate_easemytrip():
    with sync_playwright() as p:
        # Launch browser with args to start maximized
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context with no viewport (uses full screen)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        # Navigate to Easemytrip
        page.goto("https://www.easemytrip.com/")
        
        # Wait for page to load completely
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # Click on 'FROM' field
        page.locator("#FromSector_show").wait_for(state="visible")
        page.locator("#FromSector_show").click(force=True)
        time.sleep(1)
        
        # Enter New Delhi in FROM field
        page.locator("#a_FromSector_show").fill("New Delhi")
        time.sleep(2)
        
        # Click on New Delhi (DEL) from Top Cities section - using multiple approaches
        try:
            # Wait for the dropdown to be visible
            page.wait_for_selector("#fromautoFill", state="visible", timeout=5000)
            # Try clicking using text content that includes DEL
            page.locator("#fromautoFill li:has-text('DEL')").first.click()
        except:
            # Fallback: try another selector
            page.locator("#spnFromSector").click()
        
        time.sleep(1)
        
        # Click on 'TO' field
        page.locator("#Editbox13_show").wait_for(state="visible")
        page.locator("#Editbox13_show").click(force=True)
        time.sleep(1)
        
        # Enter Mumbai in TO field
        page.locator("#a_Editbox13_show").fill("Mumbai")
        time.sleep(2)
        
        # Click on Mumbai (BOM) from Top Cities section
        try:
            # Wait for the dropdown to be visible
            page.wait_for_selector("#toautoFill", state="visible", timeout=5000)
            # Try clicking using text content that includes BOM
            page.locator("#toautoFill li:has-text('BOM')").first.click()
        except:
            # Fallback: try another selector
            page.locator("#spnToSector").click()
        
        # Keep browser open to see results
        time.sleep(5)
        
        browser.close()

if __name__ == "__main__":
    automate_easemytrip()