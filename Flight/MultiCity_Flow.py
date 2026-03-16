from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os

def search_flight():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(60000)
        page.goto("https://www.easemytrip.com/", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        print("\n=== FLIGHT SEARCH AUTOMATION ===\n")
        
        # Step 0: Click on Multicity and Add City button
        try:
            page.locator("#mcity").click(force=True)
            print("✓ Multicity (id='mcity') clicked")
            page.wait_for_timeout(1000)
            
            page.locator(".addctybtn.ad").first.click(force=True)
            print("✓ Add City button clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Multicity flow error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(1000)
        
        print("\n=== MULTICITY MODE ACTIVATED ===")
        print("✓ Ready to fill From/To fields for multiple city combinations")
        print("Waiting for next instructions...")
        
        # Keep browser open to wait for further instructions
        page.wait_for_timeout(2000)
        
        # Step 1: Fill Hyderabad in From field (Multicity - mul1)
        try:
            page.locator("#FromSector-mul1_show").click(force=True)
            print("✓ From field (mul1) clicked")
            page.wait_for_timeout(500)
            
            page.type("#a_FromSector-mul1_show", "Hyderabad", delay=50)
            print("✓ From field: Hyderabad typed")
            page.wait_for_timeout(600)
            
            page.locator("li").filter(has_text="Hyderabad").first.click()
            print("✓ From: Hyderabad selected")
        except Exception as e:
            print(f"✗ From field (mul1) error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 2: Fill Pune in To field (Multicity - mul1)
        try:
            page.locator("#ToSector-mul1_show").click(force=True)
            print("✓ To field (mul1) clicked")
            page.wait_for_timeout(500)
            
            page.type("#a_ToSector-mul1_show", "Pune", delay=50)
            print("✓ To field: Pune typed")
            page.wait_for_timeout(600)
            
            page.locator("li").filter(has_text="Pune").first.click()
            print("✓ To: Pune selected")
        except Exception as e:
            print(f"✗ To field (mul1) error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 3: Fill Kolkata in second To field (Multicity - mul2)
        try:
            page.locator("#ToSector-mul2_show").click(force=True)
            print("✓ To field (mul2) clicked")
            page.wait_for_timeout(500)
            
            page.type("#a_ToSector-mul2_show", "Kolkata", delay=50)
            print("✓ To field (mul2): Kolkata typed")
            page.wait_for_timeout(600)
            
            page.locator("li").filter(has_text="Kolkata").first.click()
            print("✓ To (mul2): Kolkata selected")
        except Exception as e:
            print(f"✗ To field (mul2) error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 4: Fill Hyderabad in third To field (Multicity - mul3)
        try:
            page.locator("#ToSector-mul3_show").click(force=True)
            print("✓ To field (mul3) clicked")
            page.wait_for_timeout(500)
            
            page.type("#a_ToSector-mul3_show", "Hyderabad", delay=50)
            print("✓ To field (mul3): Hyderabad typed")
            page.wait_for_timeout(600)
            
            page.locator("#sector-sec3 #spnHyderabad").click(force=True)
            print("✓ To (mul3): Hyderabad selected")
        except Exception as e:
            print(f"✗ To field (mul3) error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 5: Fill departure dates for Multicity flights using JavaScript SelectDate function
        try:
            # Calculate dates
            first_date = datetime.now() + timedelta(days=10)
            second_date = first_date + timedelta(days=3)
            third_date = first_date + timedelta(days=6)
            
            first_date_str = first_date.strftime("%d/%m/%Y")
            first_date_id = f"trd_5_{first_date_str}"
            
            second_date_str = second_date.strftime("%d/%m/%Y")
            second_date_id = f"trd_5_{second_date_str}"
            
            third_date_str = third_date.strftime("%d/%m/%Y")
            third_date_id = f"trd_5_{third_date_str}"
            
            print(f"✓ First date (mul1): {first_date_str} (10 days from today)")
            print(f"✓ Second date (mul2): {second_date_str} (3 days after first date)")
            print(f"✓ Third date (mul3): {third_date_str} (6 days after first date)")
            
            # Fill first date using JavaScript SelectDate function
            page.locator("#ddateMul1").click(force=True)
            print("✓ First date field clicked")
            page.wait_for_timeout(800)
            
            page.evaluate(f"SelectDate('{first_date_id}')")
            print(f"✓ First date selected: {first_date_str}")
            page.wait_for_timeout(600)
            
            # Fill second date using JavaScript SelectDate function
            page.locator("#ddateMul2").click(force=True)
            print("✓ Second date field clicked")
            page.wait_for_timeout(800)
            
            page.evaluate(f"SelectDate('{second_date_id}')")
            print(f"✓ Second date selected: {second_date_str}")
            page.wait_for_timeout(600)
            
            # Fill third date using JavaScript SelectDate function
            page.locator("#ddateMul3").click(force=True)
            print("✓ Third date field clicked")
            page.wait_for_timeout(800)
            
            page.evaluate(f"SelectDate('{third_date_id}')")
            print(f"✓ Third date selected: {third_date_str}")
            page.wait_for_timeout(600)
            
        except Exception as e:
            print(f"✗ Date selection error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 6: Click Search button
        try:
            page.locator("#addmul3").click(force=True)
            print("✓ Search button clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Search button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(1000)
        
        # Step 6.5: Take screenshot of search results page
        try:
            screenshot_dir = r"D:\EMT_Flight_Playwright\Test_cases\ScreenShot"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"search_results_{timestamp}.png")
            
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"✗ Screenshot error: {e}")
        
        page.wait_for_timeout(2000)
        
        # Step 6: Click Book Now button
        try:
            page.locator(".slt-st").first.click(force=True)
            print("✓ Book Now button clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Book Now button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(1000)
        
        # Step 7: Click on ₹ 50 charity donation button (for="plant_item4")
        try:
            page.locator('label[for="plant_item4"]').click(force=True)
            print("✓ ₹ 50 charity donation (plant_item4) clicked")
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"✗ Charity donation button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(1000)
        
        # Step 8: Select 'Mr' from Title dropdown
        try:
            page.locator("#titleAdult0").select_option("Mr")
            print("✓ Title: Mr selected")
            page.wait_for_timeout(600)
        except Exception as e:
            print(f"✗ Title selection error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 9: Enter First Name 'Manni'
        try:
            page.locator("#txtFNAdult0").click(force=True)
            print("✓ First Name field (txtFNAdult0) clicked")
            page.wait_for_timeout(300)
            
            page.locator("#txtFNAdult0").fill("Manni")
            print("✓ First Name: Manni entered")
            page.wait_for_timeout(500)
        except Exception as e:
            print(f"✗ First Name entry error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 10: Enter Last Name 'Test'
        try:
            page.locator("#txtLNAdult0").click(force=True)
            print("✓ Last Name field (txtLNAdult0) clicked")
            page.wait_for_timeout(300)
            
            page.locator("#txtLNAdult0").fill("Test")
            print("✓ Last Name: Test entered")
            page.wait_for_timeout(500)
        except Exception as e:
            print(f"✗ Last Name entry error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 11: Enter Email Address 'Test@easemytrip.com'
        try:
            page.locator("#txtEmailId").click(force=True)
            print("✓ Email field (txtEmailId) clicked")
            page.wait_for_timeout(300)
            
            page.locator("#txtEmailId").fill("Test@easemytrip.com")
            print("✓ Email Address: Test@easemytrip.com entered")
            page.wait_for_timeout(500)
        except Exception as e:
            print(f"✗ Email entry error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 12: Enter Mobile Number '9999999999'
        try:
            page.locator("#txtCPhone").click(force=True)
            print("✓ Mobile Number field (txtCPhone) clicked")
            page.wait_for_timeout(300)
            
            page.locator("#txtCPhone").fill("9999999999")
            print("✓ Mobile Number: 9999999999 entered")
            page.wait_for_timeout(500)
        except Exception as e:
            print(f"✗ Mobile Number entry error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 13: Click Continue Booking button
        try:
            page.locator("#spnTransaction").click(force=True)
            print("✓ Continue Booking button (spnTransaction) clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Continue Booking button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(3000)
        
        # Step 14: Click Skip button
        try:
            page.wait_for_selector(".skipbtn", timeout=5000)
            page.locator(".skipbtn").first.click(force=True)
            print("✓ Skip button (skipbtn) clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Skip button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(1000)
        
        # Step 15: Click Skip to Payment button
        try:
            page.locator("#skipPop").click(force=True)
            print("✓ Skip to Payment button (skipPop) clicked")
            page.wait_for_timeout(4000)
        except Exception as e:
            print(f"✗ Skip to Payment button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(2000)
        
        # Step 16: Click on payment option 'Choose Mobikwik, Payzapp, PhonePe or Amazon'
        try:
            page.wait_for_selector("text=Choose Mobikwik, Payzapp, PhonePe or Amazon", timeout=10000)
            page.get_by_text("Choose Mobikwik, Payzapp, PhonePe or Amazon").click(force=True)
            print("✓ Payment option (Mobikwik, Payzapp, PhonePe, Amazon) clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Payment option error: {e}")
            current_url = page.url
            print(f"ℹ Current URL: {current_url}")
            browser.close()
            return
        
        page.wait_for_timeout(1000)
        
        # Step 17: Click on 'Bajaj Pay' option (click label instead of radio button)
        try:
            page.evaluate("document.getElementById('rdoBajaj Pay').click();")
            print("✓ Bajaj Pay radio button (rdoBajaj Pay) clicked")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"✗ Bajaj Pay selection error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(2000)
        
        # Step 18: Click on 'Make Payment' button (scroll and click)
        try:
            page.evaluate("""
                // Find the button and scroll it into view
                const btn = document.querySelector('.mk-pym4');
                if (btn && btn.offsetParent !== null) {
                    btn.scrollIntoView({behavior: 'smooth', block: 'center'});
                }
            """)
            page.wait_for_timeout(1500)
            
            # Try clicking with Playwright
            try:
                page.locator(".mk-pym4").click(force=True, timeout=5000)
                print("✓ Make Payment button (mk-pym4) clicked via Playwright")
            except:
                page.evaluate("document.querySelector('.mk-pym4').click();")
                print("✓ Make Payment button clicked via JavaScript")
            
            # Wait for page to load or navigate
            page.wait_for_timeout(3000)
            
            # Check current URL to verify if payment gateway loaded
            current_url = page.url
            print(f"✓ Current URL: {current_url}")
            
            # Look for payment gateway indicators
            page.wait_for_timeout(2000)
            
            # Check if order ID exists in URL (means checkout was processed)
            if "orderid=" in current_url:
                print("✓ ORDER PROCESSED - Order ID found in URL")
                print(f"✓ Make Payment button successfully triggered payment processing")
            else:
                print("⚠ No order ID in URL")
                
        except Exception as e:
            print(f"✗ Make Payment button error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(2000)
        
        # Step 19: Take screenshot of payment gateway page
        try:
            screenshot_dir = r"D:\EMT_Flight_Playwright\Test_cases\ScreenShot"
            os.makedirs(screenshot_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"payment_gateway_{timestamp}.png")
            
            page.screenshot(path=screenshot_path)
            print(f"✓ Screenshot saved: {screenshot_path}")
        except Exception as e:
            print(f"✗ Screenshot error: {e}")
        
        page.wait_for_timeout(1000)
        
        # TODO: Add other steps based on user instructions
        
        browser.close()

if __name__ == "__main__":
    search_flight()
