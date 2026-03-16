from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

def search_oneway_flight():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Open EaseMyTrip
        page.goto("https://www.easemytrip.com/", timeout=60000)
        print("Step 1: Opened EaseMyTrip website")
        time.sleep(5)
        
        # Fill From field
        from_field_show = page.locator("#FromSector_show")
        from_field_show.click()
        print("Step 2: Clicked on From field")
        time.sleep(1)
        
        from_field_show.type("New", delay=100)
        print("Step 3: Entered 'New' in From field")
        time.sleep(2)
        
        delhi_option = page.locator("text=New Delhi").first
        delhi_option.click()
        print("Step 4: Selected New Delhi")
        time.sleep(1)
        
        # Fill To field
        to_field_show = page.locator("#a_Editbox13_show")
        to_field_show.click()
        print("Step 5: Clicked on To field")
        time.sleep(1)
        
        to_field_show.type("BLR", delay=100)
        print("Step 6: Entered 'BLR' in To field")
        time.sleep(2)
        
        bangalore_option = page.locator("text=Bengaluru").first
        bangalore_option.click()
        print("Step 7: Selected Bengaluru")
        time.sleep(1)
        
        # Close modals
        page.press("body", "Escape")
        time.sleep(2)
        
        # Click on Departure Date
        departure_date_field = page.locator("#ddate")
        departure_date_field.click(force=True)
        print("Step 8: Clicked on Departure Date field")
        time.sleep(2)
        
        # Select date 10 days from today
        target_date = datetime.now() + timedelta(days=10)
        target_date_str = target_date.strftime("%d/%m/%Y")
        day_only = target_date.strftime("%d")
        
        print(f"Step 9: Today's date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Step 9: Target date (10 days from today): {target_date.strftime('%Y-%m-%d')}")
        
        # Use date picker calendar - try multiple selector patterns
        try:
            date_selected = False
            
            # Try pattern 1: span with day number
            day_locators = page.locator("//span[text()='" + day_only + "']").all()
            if day_locators:
                for day_elem in day_locators:
                    # Check if this is a clickable calendar day
                    parent_class = page.evaluate("(el) => el.parentElement.className", day_elem.element_handle())
                    if "day" in parent_class or "date" in parent_class or parent_class:
                        day_elem.click()
                        print(f"Step 9: Clicked day {day_only} in calendar")
                        time.sleep(2)
                        date_selected = True
                        break
            
            # Try pattern 2: div with specific day class
            if not date_selected:
                day_divs = page.locator(f"//div[contains(@class, 'day') and text()='{day_only}']").all()
                if day_divs:
                    day_divs[0].click()
                    print(f"Step 9: Clicked day {day_only} using day class selector")
                    time.sleep(2)
                    date_selected = True
            
            # Try pattern 3: button or clickable element with day number
            if not date_selected:
                clickables = page.locator(f"//button[text()='{day_only}'] | //a[text()='{day_only}']").all()
                if clickables:
                    clickables[0].click()
                    print(f"Step 9: Clicked day {day_only} as button/link")
                    time.sleep(2)
                    date_selected = True
            
            # Fallback: Direct JavaScript approach using date input
            if not date_selected:
                print("Step 9: Calendar picker patterns not found, using direct JavaScript input")
                page.evaluate(f"""
                    () => {{
                        let dateField = document.getElementById('ddate');
                        if(dateField) {{
                            dateField.value = '{target_date_str}';
                            dateField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            dateField.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            dateField.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                        }}
                    }}
                """)
                print(f"Step 9: Set date via JavaScript: {target_date_str}")
                time.sleep(2)
                
        except Exception as e:
            print(f"Step 9: Error with date selection: {e}")
            # Final fallback: clear and type
            departure_date_field.fill("")
            time.sleep(0.5)
            departure_date_field.type(target_date_str, delay=100)
            print(f"Step 9: Typed date: {target_date_str}")
            time.sleep(2)
        
        # Verify the date was set correctly
        actual_date = departure_date_field.input_value()
        print(f"Step 9: Verification - Date field now contains: {actual_date}")
        
        if actual_date != target_date_str:
            print(f"Step 9: WARNING - Date mismatch! Expected {target_date_str}, got {actual_date}")
        
        time.sleep(1)
        print("Step 10: Selected 1 Adult (default)")
        time.sleep(1)
        
        # Click Search button directly
        print("Step 11: Clicking Search button...")
        try:
            # Use the exact selector with class srchBtnSe
            search_button = page.locator("input[type='button'][value='Search'].srchBtnSe")
            if search_button.is_visible():
                search_button.click()
                print("Step 11: Clicked Search button")
            else:
                # Try using querySelector
                page.evaluate("document.querySelector('.srchBtnSe').click()")
                print("Step 11: Clicked Search button using JavaScript")
            time.sleep(5)
        except Exception as e:
            print(f"Step 11: Error clicking Search button: {e}")
            time.sleep(5)
        
        # Wait for results
        print("Step 12: Waiting for flight results...")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(3)
        print("Step 12: Flight results loaded")
        
        # Click Book Now
        print("Step 13: Clicking Book Now...")
        try:
            # Click using class selector first
            book_now_button = page.locator("._mfbookbtn").first
            if book_now_button.is_visible():
                # Scroll into view using JavaScript
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, book_now_button.element_handle())
                time.sleep(1)
                book_now_button.click()
                print("Step 13: Clicked Book Now button")
            else:
                print("Step 13: Book Now button not visible, trying alternative selector...")
                # Try alternative selectors if the main one fails
                book_buttons = page.locator("//button[contains(text(), 'Book Now')]").all()
                if book_buttons:
                    page.evaluate("""
                        (el) => {
                            el.scrollIntoView(true);
                        }
                    """, book_buttons[0].element_handle())
                    time.sleep(1)
                    book_buttons[0].click()
                    print("Step 13: Clicked Book Now for first airline")
                else:
                    book_links = page.locator("//a[contains(text(), 'Book Now')]").all()
                    if book_links:
                        page.evaluate("""
                            (el) => {
                                el.scrollIntoView(true);
                            }
                        """, book_links[0].element_handle())
                        time.sleep(1)
                        book_links[0].click()
                        print("Step 13: Clicked Book Now link for first airline")
                    else:
                        page.evaluate("""
                            Array.from(document.querySelectorAll('button, a')).find(el => 
                                el.innerText && el.innerText.includes('Book')
                            )?.click()
                        """)
                        print("Step 13: Clicked Book Now using JavaScript")
        except Exception as e:
            print(f"Step 13: Error clicking Book Now: {e}")
        
        time.sleep(5)

        # Check for "More Fare Options Available" page and click Book Now
        print("Step 13.5: Checking for More Fare Options Available page...")
        try:
            # Check if we're on the More Fare Options page by looking for the section or using JavaScript
            is_more_fare_page = page.evaluate("""
                () => {
                    return document.querySelector('._mfpoupbx') !== null || 
                           document.body.innerText.includes('More Fare Options');
                }
            """)
            
            if is_more_fare_page:
                print("Step 13.5: Found More Fare Options Available page")
                time.sleep(2)
                
                # Click Book Now button using the specific XPath selector for this page
                book_now_link = page.locator("(//a[contains(@class,'_mfbookbtn') and normalize-space()='Book Now'])[1]")
                if book_now_link.is_visible():
                    page.evaluate("""
                        (el) => {
                            el.scrollIntoView(true);
                        }
                    """, book_now_link.element_handle())
                    time.sleep(1)
                    book_now_link.click()
                    print("Step 13.5: Clicked Book Now on More Fare Options page using XPath")
                    time.sleep(3)
                else:
                    print("Step 13.5: Book Now link not visible with XPath, trying alternative selector...")
                    # Try alternative selectors
                    book_button_alt = page.locator("a:has-text('Book Now')").first
                    if book_button_alt.is_visible():
                        page.evaluate("""
                            (el) => {
                                el.scrollIntoView(true);
                            }
                        """, book_button_alt.element_handle())
                        time.sleep(1)
                        book_button_alt.click()
                        print("Step 13.5: Clicked Book Now using alternative selector")
                        time.sleep(3)
                    else:
                        page.evaluate("""
                            () => {
                                let links = document.querySelectorAll('a._mfbookbtn');
                                if(links.length > 0) {
                                    links[0].click();
                                    return true;
                                }
                                let bookLinks = Array.from(document.querySelectorAll('a')).find(a => a.textContent.trim() === 'Book Now');
                                if(bookLinks) {
                                    bookLinks.click();
                                    return true;
                                }
                            }
                        """)
                        print("Step 13.5: Clicked Book Now using JavaScript")
                        time.sleep(3)
            else:
                print("Step 13.5: More Fare Options Available page not found")
        except Exception as e:
            print(f"Step 13.5: Error on More Fare Options page: {e}")
        
        print("Step 14: Waiting for booking page...")
        page.wait_for_load_state("domcontentloaded")
        print("Step 14: Booking page loaded successfully!")
        
        # Click on ACKO insurance 'Yes, I want to secure my trip with insurance.' radio button
        print("Step 15: Looking for ACKO insurance option...")
        
        try:
            # First, find the ACKO insurance section
            acko_section = page.locator("text=ACKO").first
            if acko_section.is_visible():
                print("Step 15: Found ACKO insurance section")
                
                # Look for the radio button with "Yes, I want to secure my trip with insurance" 
                # within or near the ACKO section
                insurance_yes_buttons = page.locator("//input[@type='radio' and @name='InsuranceYesNo'] | //label[contains(text(), 'Yes, I want to secure my trip')]").all()
                
                if insurance_yes_buttons:
                    print(f"Step 15: Found {len(insurance_yes_buttons)} insurance yes buttons")
                    # Click the first one (ACKO insurance)
                    insurance_yes_buttons[0].click()
                    print("Step 15: Clicked 'Yes, I want to secure my trip with insurance' for ACKO")
                    time.sleep(2)
                else:
                    # Try alternative selector
                    print("Step 15: Trying alternative selector for insurance radio button...")
                    insurance_radio = page.locator("//input[@type='radio']").filter(has_text="Yes").first
                    if insurance_radio.is_visible():
                        insurance_radio.click()
                        print("Step 15: Clicked insurance yes radio button")
                        time.sleep(2)
                    else:
                        # Try using JavaScript to find and click
                        page.evaluate("""
                            () => {
                                let radios = document.querySelectorAll('input[type="radio"]');
                                for(let radio of radios) {
                                    let label = radio.nextElementSibling;
                                    if(label && label.innerText && label.innerText.includes('Yes, I want')) {
                                        radio.click();
                                        return true;
                                    }
                                }
                            }
                        """)
                        print("Step 15: Clicked insurance yes radio button using JavaScript")
                        time.sleep(2)
            else:
                print("Step 15: ACKO insurance section not found")
        except Exception as e:
            print(f"Step 15: Error selecting ACKO insurance: {e}")
        
        time.sleep(3)
        
        # Click on Title dropdown and select Mr
        print("Step 16: Selecting passenger title...")
        
        try:
            # Find the title dropdown with id="titleAdult0"
            title_dropdown = page.locator("#titleAdult0")
            if title_dropdown.is_visible():
                title_dropdown.click()
                print("Step 16: Clicked on Title dropdown")
                time.sleep(1)
                
                # Select "Mr" option with value="Mr"
                mr_option = page.locator("//option[@value='Mr']").first
                if mr_option.is_visible():
                    mr_option.click()
                    print("Step 16: Selected 'Mr' from title dropdown")
                    time.sleep(1)
                else:
                    # Try alternative selector
                    mr_option = page.locator("select#titleAdult0 option").filter(has_text="Mr").first
                    if mr_option.is_visible():
                        mr_option.click()
                        print("Step 16: Selected 'Mr' from title dropdown")
                        time.sleep(1)
                    else:
                        # Try using JavaScript to select the option
                        page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('titleAdult0');
                                if(dropdown) {
                                    for(let option of dropdown.options) {
                                        if(option.value === 'Mr') {
                                            dropdown.value = 'Mr';
                                            dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                            return true;
                                        }
                                    }
                                }
                            }
                        """)
                        print("Step 16: Selected 'Mr' using JavaScript")
                        time.sleep(1)
            else:
                print("Step 16: Title dropdown not found")
        except Exception as e:
            print(f"Step 16: Error selecting title: {e}")
        
        time.sleep(2)
        
        # Click on First Name field and enter "Manni"
        print("Step 17: Entering first name...")
        
        try:
            # Find the first name input field with name="txtFNAdult0"
            first_name_field = page.locator("input[name='txtFNAdult0']")
            if first_name_field.is_visible():
                first_name_field.click()
                print("Step 17: Clicked on First Name field")
                time.sleep(0.5)
                
                # Clear any existing text
                first_name_field.fill("")
                time.sleep(0.3)
                
                # Type "Manni"
                first_name_field.type("Manni", delay=100)
                print("Step 17: Entered 'Manni' in First Name field")
                
                # Verify the text was entered
                actual_name = first_name_field.input_value()
                print(f"Step 17: Verification - First Name field now contains: {actual_name}")
                time.sleep(1)
            else:
                print("Step 17: First Name field not found")
        except Exception as e:
            print(f"Step 17: Error entering first name: {e}")
        
        time.sleep(2)
        
        # Click on Last Name field and enter "Test"
        print("Step 18: Entering last name...")
        
        try:
            # Find the last name input field with class="input_trvl"
            # We need to find the one that's for last name (usually after first name)
            last_name_fields = page.locator("input.input_trvl")
            
            if last_name_fields:
                # Get all input_trvl fields and find the one that's not the first name
                all_trvl_inputs = last_name_fields.all()
                
                # The last name field should be the second one after first name
                if len(all_trvl_inputs) > 1:
                    last_name_field = all_trvl_inputs[1]
                else:
                    last_name_field = last_name_fields.first
                
                if last_name_field.is_visible():
                    last_name_field.click()
                    print("Step 18: Clicked on Last Name field")
                    time.sleep(0.5)
                    
                    # Clear any existing text
                    last_name_field.fill("")
                    time.sleep(0.3)
                    
                    # Type "Test"
                    last_name_field.type("Test", delay=100)
                    print("Step 18: Entered 'Test' in Last Name field")
                    
                    # Verify the text was entered
                    actual_name = last_name_field.input_value()
                    print(f"Step 18: Verification - Last Name field now contains: {actual_name}")
                    time.sleep(1)
                else:
                    print("Step 18: Last Name field not visible")
            else:
                print("Step 18: Last Name field not found")
        except Exception as e:
            print(f"Step 18: Error entering last name: {e}")
        
        time.sleep(2)
        
        # Click on Email Address field and enter email
        print("Step 19: Entering email address...")
        
        try:
            # Find the email input field with id="txtEmailId"
            email_field = page.locator("input#txtEmailId")
            if email_field.is_visible():
                email_field.click()
                print("Step 19: Clicked on Email Address field")
                time.sleep(0.5)
                
                # Clear any existing text
                email_field.fill("")
                time.sleep(0.3)
                
                # Type the email
                email_field.type("manish.dasila@easemytrip.com", delay=50)
                print("Step 19: Entered 'manish.dasila@easemytrip.com' in Email Address field")
                
                # Verify the email was entered
                actual_email = email_field.input_value()
                print(f"Step 19: Verification - Email Address field now contains: {actual_email}")
                time.sleep(1)
            else:
                print("Step 19: Email Address field not found")
        except Exception as e:
            print(f"Step 19: Error entering email address: {e}")
        
        time.sleep(2)
        
        # Click on Mobile Number field and enter mobile number
        print("Step 20: Entering mobile number...")
        
        try:
            # Find the mobile number input field with id="txtCPhone"
            mobile_field = page.locator("input#txtCPhone")
            if mobile_field.is_visible():
                mobile_field.click()
                print("Step 20: Clicked on Mobile Number field")
                time.sleep(0.5)
                
                # Clear any existing text
                mobile_field.fill("")
                time.sleep(0.3)
                
                # Type the mobile number
                mobile_field.type("9999999999", delay=50)
                print("Step 20: Entered '9999999999' in Mobile Number field")
                
                # Verify the mobile number was entered
                actual_mobile = mobile_field.input_value()
                print(f"Step 20: Verification - Mobile Number field now contains: {actual_mobile}")
                time.sleep(1)
            else:
                print("Step 20: Mobile Number field not found")
        except Exception as e:
            print(f"Step 20: Error entering mobile number: {e}")
        
        time.sleep(2)
        
        # Click on Continue Booking button
        print("Step 21: Clicking Continue Booking button...")
        
        try:
            # Find the Continue Booking button with id="spnTransaction"
            continue_booking_btn = page.locator("#spnTransaction")
            if continue_booking_btn.is_visible():
                continue_booking_btn.click()
                print("Step 21: Clicked Continue Booking button")
                time.sleep(3)
            else:
                print("Step 21: Continue Booking button not visible, trying alternative selector...")
                # Try with button selector
                continue_btn = page.locator("button#spnTransaction, span#spnTransaction").first
                if continue_btn.is_visible():
                    continue_btn.click()
                    print("Step 21: Clicked Continue Booking button (alternative selector)")
                    time.sleep(3)
                else:
                    # Try using JavaScript
                    page.evaluate("""
                        () => {
                            let btn = document.getElementById('spnTransaction');
                            if(btn) {
                                btn.click();
                                return true;
                            }
                        }
                    """)
                    print("Step 21: Clicked Continue Booking button using JavaScript")
                    time.sleep(3)
        except Exception as e:
            print(f"Step 21: Error clicking Continue Booking button: {e}")
        
        # Wait for seat selection popup to appear
        print("Step 22: Waiting for seat selection popup...")
        time.sleep(3)
        
        # Click on Edit button in the "We have chosen the best seat specially for you" popup
        print("Step 23: Clicking Edit button on seat popup...")
        
        try:
            # Find the Edit button with class="edit_btn"
            edit_btn = page.locator("button.edit_btn, .edit_btn, [class*='edit_btn']").first
            if edit_btn.is_visible():
                edit_btn.click()
                print("Step 23: Clicked Edit button on seat popup")
                time.sleep(3)
            else:
                print("Step 23: Edit button not visible, trying alternative selectors...")
                # Try with span or other elements
                edit_elements = page.locator("[class*='edit']")
                if edit_elements.count() > 0:
                    for i in range(edit_elements.count()):
                        elem = edit_elements.nth(i)
                        text = elem.inner_text()
                        if "edit" in text.lower():
                            elem.click()
                            print("Step 23: Clicked Edit button (alternative selector)")
                            time.sleep(3)
                            break
                else:
                    # Try using JavaScript to find and click
                    page.evaluate("""
                        () => {
                            let btn = document.querySelector('button.edit_btn');
                            if(btn) {
                                btn.click();
                                return true;
                            }
                            let editBtn = document.querySelector('[class*="edit_btn"]');
                            if(editBtn) {
                                editBtn.click();
                                return true;
                            }
                        }
                    """)
                    print("Step 23: Clicked Edit button using JavaScript")
                    time.sleep(3)
        except Exception as e:
            print(f"Step 23: Error clicking Edit button: {e}")
        
        # Wait for next page to load
        print("Step 24: Waiting for seat selection page to load...")
        try:
            page.wait_for_load_state("domcontentloaded")
        except:
            pass
        time.sleep(3)
        print("Step 24: Seat selection page loaded successfully!")
        
        # Click on Skip to Payment button
        print("Step 25: Clicking Skip to Payment button...")
        
        try:
            # First, close any overlays that might be blocking the button
            page.evaluate("""
                () => {
                    let overlay = document.querySelector('.revw_opcty');
                    if(overlay) {
                        overlay.style.display = 'none';
                    }
                }
            """)
            time.sleep(1)
            
            # Find the Skip to Payment button with id="skipPop"
            skip_btn = page.locator("#skipPop")
            if skip_btn.is_visible():
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, skip_btn.element_handle())
                time.sleep(1)
                skip_btn.click()
                print("Step 25: Clicked Skip to Payment button")
                time.sleep(3)
            else:
                print("Step 25: Skip to Payment button not visible, trying alternative selectors...")
                # Try with class selector
                skip_alt = page.locator(".skipotp.ng-star-inserted")
                if skip_alt.is_visible():
                    page.evaluate("""
                        (el) => {
                            el.scrollIntoView(true);
                        }
                    """, skip_alt.element_handle())
                    time.sleep(1)
                    skip_alt.click()
                    print("Step 25: Clicked Skip to Payment button (class selector)")
                    time.sleep(3)
                else:
                    # Try using JavaScript
                    page.evaluate("""
                        () => {
                            let btn = document.getElementById('skipPop');
                            if(btn) {
                                btn.scrollIntoView(true);
                                btn.click();
                                return true;
                            }
                            let skipBtn = document.querySelector('.skipotp.ng-star-inserted');
                            if(skipBtn) {
                                skipBtn.scrollIntoView(true);
                                skipBtn.click();
                                return true;
                            }
                        }
                    """)
                    print("Step 25: Clicked Skip to Payment button using JavaScript")
                    time.sleep(3)
        except Exception as e:
            print(f"Step 25: Error clicking Skip to Payment button: {e}")
        
        # Wait for payment page to load
        print("Step 26: Waiting for payment page to load...")
        try:
            page.wait_for_load_state("domcontentloaded")
        except:
            pass
        time.sleep(3)
        print("Step 26: Payment page loaded successfully!")
        
        # Click on wallet payment option
        print("Step 27: Clicking on wallet payment option...")
        
        try:
            # Find the wallet button with class="wallet-txt PG2 blu"
            wallet_btn = page.locator(".wallet-txt.PG2.blu")
            if wallet_btn.is_visible():
                wallet_btn.click()
                print("Step 27: Clicked on wallet payment option")
                time.sleep(3)
            else:
                print("Step 27: Wallet button not visible, trying alternative selectors...")
                # Try with different selector combinations
                wallet_alt = page.locator("[class*='wallet-txt'], [class*='PG2'], [class*='blu']").first
                if wallet_alt.is_visible():
                    wallet_alt.click()
                    print("Step 27: Clicked on wallet payment option (alternative selector)")
                    time.sleep(3)
                else:
                    # Try using JavaScript
                    page.evaluate("""
                        () => {
                            let btn = document.querySelector('.wallet-txt.PG2.blu');
                            if(btn) {
                                btn.click();
                                return true;
                            }
                            let walletBtn = document.querySelector('[class*="wallet-txt"]');
                            if(walletBtn) {
                                walletBtn.click();
                                return true;
                            }
                        }
                    """)
                    print("Step 27: Clicked on wallet payment option using JavaScript")
                    time.sleep(3)
        except Exception as e:
            print(f"Step 27: Error clicking wallet payment option: {e}")
        
        # Wait for wallet selection page to load
        print("Step 28: Waiting for wallet selection page to load...")
        try:
            page.wait_for_load_state("domcontentloaded")
        except:
            pass
        time.sleep(3)
        print("Step 28: Wallet selection page loaded successfully!")
        
        # Click on Bajaj Pay radio button
        print("Step 29: Clicking on Bajaj Pay radio button...")
        
        try:
            # Find the Bajaj Pay radio button with id="rdoBajaj Pay"
            bajaj_pay_btn = page.locator("#rdoBajaj Pay")
            if bajaj_pay_btn.is_visible():
                bajaj_pay_btn.click()
                print("Step 29: Clicked on Bajaj Pay radio button")
                time.sleep(2)
            else:
                print("Step 29: Bajaj Pay radio button not visible, trying alternative selectors...")
                # Try with different selector combinations
                bajaj_alt = page.locator("input[id*='Bajaj'], [name*='Bajaj'], label:has-text('Bajaj Pay')").first
                if bajaj_alt.is_visible():
                    bajaj_alt.click()
                    print("Step 29: Clicked on Bajaj Pay radio button (alternative selector)")
                    time.sleep(2)
                else:
                    # Try using JavaScript
                    page.evaluate("""
                        () => {
                            let btn = document.getElementById('rdoBajaj Pay');
                            if(btn) {
                                btn.click();
                                return true;
                            }
                            let bajajBtn = document.querySelector('[id*="Bajaj"]');
                            if(bajajBtn) {
                                bajajBtn.click();
                                return true;
                            }
                        }
                    """)
                    print("Step 29: Clicked on Bajaj Pay radio button using JavaScript")
                    time.sleep(2)
        except Exception as e:
            print(f"Step 29: Error clicking Bajaj Pay radio button: {e}")
        
        # Wait for next page to load
        print("Step 30: Waiting for payment processing...")
        try:
            page.wait_for_load_state("domcontentloaded")
        except:
            pass
        time.sleep(3)
        print("Step 30: Bajaj Pay selected successfully!")
        
        # Click on Make Payment button
        print("Step 31: Clicking on Make Payment button...")
        
        try:
            # Try with the specific ID selector first - this is the main Make Payment button
            make_payment_id = page.locator("#makpbtn")
            if make_payment_id.is_visible():
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, make_payment_id.element_handle())
                time.sleep(1)
                make_payment_id.click()
                print("Step 31: Clicked on Make Payment button")
                time.sleep(3)
            else:
                print("Step 31: Make Payment button not visible with ID, trying alternative selectors...")
                # Try with class selector (div.mk-pym4)
                make_payment_btn = page.locator("div.mk-pym4").first
                if make_payment_btn.is_visible():
                    page.evaluate("""
                        (el) => {
                            el.scrollIntoView(true);
                        }
                    """, make_payment_btn.element_handle())
                    time.sleep(1)
                    make_payment_btn.click()
                    print("Step 31: Clicked on Make Payment button (div selector)")
                    time.sleep(3)
                else:
                    # Try with button tag
                    make_payment_alt = page.locator("button.mk-pym4")
                    if make_payment_alt.is_visible():
                        page.evaluate("""
                            (el) => {
                                el.scrollIntoView(true);
                            }
                        """, make_payment_alt.element_handle())
                        time.sleep(1)
                        make_payment_alt.click()
                        print("Step 31: Clicked on Make Payment button (button selector)")
                        time.sleep(3)
                    else:
                        # Try using JavaScript
                        page.evaluate("""
                            () => {
                                let btn = document.querySelector('#makpbtn');
                                if(btn) {
                                    btn.scrollIntoView(true);
                                    btn.click();
                                    return true;
                                }
                            }
                        """)
                        print("Step 31: Clicked on Make Payment button using JavaScript")
                        time.sleep(3)
        except Exception as e:
            print(f"Step 31: Error clicking Make Payment button: {e}")
        
        # Take screenshot after Make Payment button click
        print("Step 32: Taking screenshot...")
        try:
            import os
            screenshot_dir = r"D:\EMT_Flight_Playwright\Test_cases\ScreenShot"
            
            # Create directory if it doesn't exist
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
            
            # Take screenshot with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = os.path.join(screenshot_dir, f"payment_page_{timestamp}.png")
            
            page.screenshot(path=screenshot_path)
            print(f"Step 32: Screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"Step 32: Error taking screenshot: {e}")
        
        print("\nScript completed! Keeping browser open for 10 seconds...")
        time.sleep(10)
        
        browser.close()
        print("Browser closed. Script finished.")

if __name__ == "__main__":
    search_oneway_flight()
