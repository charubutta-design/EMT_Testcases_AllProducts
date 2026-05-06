from playwright.sync_api import sync_playwright

def automate_easemytrip():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        try:
            print("[WEB] Navigating to bus.easemytrip.com...")
            page.goto("https://bus.easemytrip.com/")
            print("[OK] Website loaded successfully!")
            
            print("[AUTH] Clicking on sign-in/signup button...")
            page.locator('#divSignInPnl ._btnclick').click()
            print("[OK] Sign-in/signup button clicked!")
            page.wait_for_timeout(1000)
            
            print("[NOTE] Clicking on login button...")
            page.locator('#shwlogn').click()
            print("[OK] Login button clicked!")
            page.wait_for_timeout(1000)
            
            print("[EMAIL] Clicking on email field...")
            page.locator('//*[@id="lgnBox"]/div[1]/div[2]/div/label').click()
            print("[OK] Email field clicked!")
            
            print("[EMAIL] Entering email...")
            page.locator('//*[@id="lgnBox"]/div[1]/div[2]/div/label').fill("chetan.sharma@easemytrip.com")
            page.keyboard.press("Space")
            page.keyboard.press("Enter")
            print("[OK] Email entered and submitted!")
            page.wait_for_timeout(1500)
            
            print("[BTN] Clicking continue button...")
            page.locator('//*[@id="shwotp"]').click()
            print("[OK] Continue button clicked!")
            page.wait_for_timeout(1000)
            
            print("[AUTH] Clicking on password field...")
            page.locator('//*[@id="emailgnBox"]/div/div[2]/div/label').click()
            print("[OK] Password field clicked!")
            
            print("[AUTH] Entering password...")
            page.locator('//*[@id="emailgnBox"]/div/div[2]/div/label').fill("Chetan@123")
            print("[OK] Password entered!")
            page.wait_for_timeout(500)
            
            print("[BTN] Clicking on login button...")
            page.locator('//*[@id="emailgnBox"]/div/div[5]/input').click()
            print("[OK] Login button clicked!")
            page.wait_for_timeout(2000)
            
            print("[ERROR] Closing popup...")
            page.evaluate('document.querySelector("._crosslog._crosslogsuccess").click()')
            print("[OK] Popup closed!")
            
            print("[WAIT] Waiting for 5 seconds...")
            page.wait_for_timeout(5000)
            print("[OK] Login automation completed successfully!")
            
        except Exception as e:
            print(f"[ERROR] Error: {e}")
        
        finally:
            browser.close()

if __name__ == "__main__":
    automate_easemytrip()
