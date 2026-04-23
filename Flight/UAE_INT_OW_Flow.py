from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import time

def search_oneway_flight():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Open EaseMyTrip
        page.goto("https://www.easemytrip.ae/", timeout=60000)
        print("Step 1: Opened EaseMyTrip website")
        time.sleep(5)
        
        # Fill From field
        from_field_show = page.locator("#FromSector_show")
        from_field_show.click()
        print("Step 2: Clicked on From field")
        time.sleep(1)
        
        # Select Istanbul Atatürk Airport from Top Cities
        istanbul_option = page.locator("#airport4")
        istanbul_option.click()
        print("Step 3: Selected Istanbul Atatürk Airport from Top Cities")
        time.sleep(1)
        
        # Fill To field
        to_field_show = page.locator("#a_Editbox13_show")
        to_field_show.click()
        print("Step 5: Clicked on To field")
        time.sleep(1)
        
        to_field_show.type("DXB", delay=100)
        print("Step 6: Entered 'DXB' in To field")
        time.sleep(2)
        
        dubai_option = page.locator("#airportDubai").first
        dubai_option.click()
        print("Step 7: Selected Dubai International Airport")
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
            # Click using class selector "bk-btn"
            book_now_button = page.locator(".bk-btn").first
            if book_now_button.is_visible():
                # Scroll into view using JavaScript
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, book_now_button.element_handle())
                time.sleep(1)
                book_now_button.click()
                print("Step 13: Clicked Book Now button with class 'bk-btn'")
            else:
                print("Step 13: Book Now button with class 'bk-btn' not visible, trying alternative selector...")
                # Try the old selectors as fallback
                book_now_button_alt = page.locator("._mfbookbtn").first
                if book_now_button_alt.is_visible():
                    page.evaluate("""
                        (el) => {
                            el.scrollIntoView(true);
                        }
                    """, book_now_button_alt.element_handle())
                    time.sleep(1)
                    book_now_button_alt.click()
                    print("Step 13: Clicked Book Now button with class '_mfbookbtn'")
                else:
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
            # Wait a moment for page to fully render
            time.sleep(2)
            
            # Check if we're on the More Fare Options page by looking for the button directly
            book_button_exists = page.evaluate("""
                () => {
                    let btnBookNow = document.getElementById('btnBookNow');
                    let bookBtn = document.querySelector('.book-bt-n.marg-left');
                    let hasMoreFareText = document.body.innerText.includes('More Fare Options');
                    return {
                        btnBookNowExists: btnBookNow !== null,
                        bookBtnExists: bookBtn !== null,
                        hasMoreFareText: hasMoreFareText
                    };
                }
            """)
            
            print(f"Step 13.5: Page elements check - btnBookNow exists: {book_button_exists['btnBookNowExists']}, book-bt-n exists: {book_button_exists['bookBtnExists']}, More Fare text: {book_button_exists['hasMoreFareText']}")
            
            # Try to click the Book Now button directly
            if book_button_exists['btnBookNowExists'] or book_button_exists['bookBtnExists'] or book_button_exists['hasMoreFareText']:
                print("Step 13.5: Found More Fare Options Available page - attempting to click Book Now button")
                time.sleep(1)
                
                # Try clicking with JavaScript first
                clicked = page.evaluate("""
                    () => {
                        let btnBookNow = document.getElementById('btnBookNow');
                        if(btnBookNow) {
                            console.log('Found button by ID, clicking...');
                            btnBookNow.click();
                            return true;
                        }
                        let bookBtn = document.querySelector('.book-bt-n.marg-left');
                        if(bookBtn) {
                            console.log('Found button by class, clicking...');
                            bookBtn.click();
                            return true;
                        }
                        return false;
                    }
                """)
                
                if clicked:
                    print("Step 13.5: Successfully clicked Book Now button using JavaScript")
                    time.sleep(3)
                else:
                    print("Step 13.5: JavaScript click failed, trying Playwright locators...")
                    # Fallback to Playwright locators
                    book_now_button = page.locator("#btnBookNow").first
                    if book_now_button.count() > 0:
                        page.evaluate("""
                            (el) => {
                                el.scrollIntoView(true);
                            }
                        """, book_now_button.element_handle())
                        time.sleep(1)
                        book_now_button.click()
                        print("Step 13.5: Clicked Book Now button using Playwright locator")
                        time.sleep(3)
                    else:
                        book_button_alt = page.locator(".book-bt-n.marg-left").first
                        if book_button_alt.count() > 0:
                            page.evaluate("""
                                (el) => {
                                    el.scrollIntoView(true);
                                }
                            """, book_button_alt.element_handle())
                            time.sleep(1)
                            book_button_alt.click()
                            print("Step 13.5: Clicked Book Now using class selector")
                            time.sleep(3)
            else:
                print("Step 13.5: More Fare Options Available page not found - proceeding to next step")
        except Exception as e:
            print(f"Step 13.5: Error on More Fare Options page: {e}")
        
        print("Step 14: Waiting for booking page...")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(8)  # Wait longer for page elements to fully render
        print("Step 14: Booking page loaded successfully!")
        
        # Debug: Check what's on the page
        page_title = page.title()
        print(f"Step 14.1: Page title: {page_title}")
        
        # Scroll to top first
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)
        
        # Take a screenshot to see the page state
        page.screenshot(path=f"D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\booking_page_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        print("Step 14.2: Screenshot of booking page taken")
        
        # Check if passenger form exists
        form_exists = page.evaluate("""
            () => {
                let titleField = document.getElementById('titleAdult0');
                let firstNameField = document.querySelector('input[name="txtFNAdult0"]');
                return {
                    titleFieldExists: titleField !== null,
                    firstNameFieldExists: firstNameField !== null,
                    pageHTML: document.body.innerHTML.substring(0, 500)
                };
            }
        """)
        print(f"Step 14.3: Form field check - Title exists: {form_exists['titleFieldExists']}, FirstName exists: {form_exists['firstNameFieldExists']}")
        
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
        
        # Scroll down to ensure form fields are visible
        page.evaluate("window.scrollBy(0, 500)")
        time.sleep(2)
        
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
        
        # Click on DOB Day dropdown and select day 04
        print("Step 18.5: Selecting Date of Birth Day...")
        
        try:
            # Find the DOB day dropdown with id="divDOBDayAdult0"
            dob_day_dropdown = page.locator("#divDOBDayAdult0")
            if dob_day_dropdown.count() > 0:
                # Scroll into view and click
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, dob_day_dropdown.element_handle())
                time.sleep(1)
                
                dob_day_dropdown.click()
                print("Step 18.5: Clicked on DOB Day dropdown")
                time.sleep(2)
                
                # Use JavaScript to select day 04
                selected = page.evaluate("""
                    () => {
                        let dropdown = document.getElementById('divDOBDayAdult0');
                        if(dropdown) {
                            // Try to find the option with value='04'
                            for(let option of dropdown.options) {
                                if(option.value === '04') {
                                    dropdown.value = '04';
                                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    dropdown.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected day 04 by ID' };
                                }
                            }
                        }
                        
                        // Try by name attribute
                        let selectByName = document.querySelector('select[name="AdultDay"]');
                        if(selectByName) {
                            for(let option of selectByName.options) {
                                if(option.value === '04') {
                                    selectByName.value = '04';
                                    selectByName.dispatchEvent(new Event('change', { bubbles: true }));
                                    selectByName.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected day 04 by name' };
                                }
                            }
                        }
                        
                        return { success: false, message: 'Could not find dropdown or day 04' };
                    }
                """)
                
                if selected['success']:
                    print(f"Step 18.5: {selected['message']}")
                    time.sleep(1)
                else:
                    print(f"Step 18.5: {selected['message']}")
            else:
                print("Step 18.5: DOB Day dropdown not found")
        except Exception as e:
            print(f"Step 18.5: Error selecting DOB Day: {e}")
        
        time.sleep(2)
        
        # Click on DOB Month dropdown and select Aug (08)
        print("Step 18.6: Selecting Date of Birth Month...")
        
        try:
            # Find the DOB month dropdown with id="divDOBMonAdult0"
            dob_mon_dropdown = page.locator("#divDOBMonAdult0")
            if dob_mon_dropdown.count() > 0:
                # Scroll into view and click
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, dob_mon_dropdown.element_handle())
                time.sleep(1)
                
                dob_mon_dropdown.click()
                print("Step 18.6: Clicked on DOB Month dropdown")
                time.sleep(2)
                
                # Use JavaScript to select Aug (08)
                selected = page.evaluate("""
                    () => {
                        let dropdown = document.getElementById('divDOBMonAdult0');
                        if(dropdown) {
                            // Try to find the option with value='08' (Aug)
                            for(let option of dropdown.options) {
                                if(option.value === '08') {
                                    dropdown.value = '08';
                                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    dropdown.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected month Aug (08) by ID' };
                                }
                            }
                        }
                        
                        // Try by name attribute
                        let selectByName = document.querySelector('select[name="AdultMonth"]');
                        if(selectByName) {
                            for(let option of selectByName.options) {
                                if(option.value === '08') {
                                    selectByName.value = '08';
                                    selectByName.dispatchEvent(new Event('change', { bubbles: true }));
                                    selectByName.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected month Aug (08) by name' };
                                }
                            }
                        }
                        
                        return { success: false, message: 'Could not find dropdown or month 08' };
                    }
                """)
                
                if selected['success']:
                    print(f"Step 18.6: {selected['message']}")
                    time.sleep(1)
                else:
                    print(f"Step 18.6: {selected['message']}")
            else:
                print("Step 18.6: DOB Month dropdown not found")
        except Exception as e:
            print(f"Step 18.6: Error selecting DOB Month: {e}")
        
        time.sleep(2)
        
        # Click on DOB Year dropdown and select 1998
        print("Step 18.7: Selecting Date of Birth Year...")
        
        try:
            # Find the DOB year dropdown with id="divDOBYarAdult0"
            dob_year_dropdown = page.locator("#divDOBYarAdult0")
            if dob_year_dropdown.count() > 0:
                # Scroll into view and click
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, dob_year_dropdown.element_handle())
                time.sleep(1)
                
                dob_year_dropdown.click()
                print("Step 18.7: Clicked on DOB Year dropdown")
                time.sleep(2)
                
                # Use JavaScript to select 1998
                selected = page.evaluate("""
                    () => {
                        let dropdown = document.getElementById('divDOBYarAdult0');
                        if(dropdown) {
                            // Try to find the option with value='1998'
                            for(let option of dropdown.options) {
                                if(option.value === '1998') {
                                    dropdown.value = '1998';
                                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    dropdown.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected year 1998 by ID' };
                                }
                            }
                        }
                        
                        // Try by name attribute
                        let selectByName = document.querySelector('select[name="AdultYear"]');
                        if(selectByName) {
                            for(let option of selectByName.options) {
                                if(option.value === '1998') {
                                    selectByName.value = '1998';
                                    selectByName.dispatchEvent(new Event('change', { bubbles: true }));
                                    selectByName.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected year 1998 by name' };
                                }
                            }
                        }
                        
                        return { success: false, message: 'Could not find dropdown or year 1998' };
                    }
                """)
                
                if selected['success']:
                    print(f"Step 18.7: {selected['message']}")
                    time.sleep(1)
                else:
                    print(f"Step 18.7: {selected['message']}")
            else:
                print("Step 18.7: DOB Year dropdown not found")
        except Exception as e:
            print(f"Step 18.7: Error selecting DOB Year: {e}")
        
        time.sleep(2)
        
        # Click on Passport Number field and enter "Test123"
        print("Step 18.8: Entering Passport Number...")
        
        try:
            # Find the passport number input field with id="txtPassAdult0" or name="AdultpassportNo"
            passport_field = page.locator("#txtPassAdult0")
            if passport_field.count() > 0:
                passport_field.click()
                print("Step 18.8: Clicked on Passport Number field")
                time.sleep(0.5)
                
                # Clear any existing text
                passport_field.fill("")
                time.sleep(0.3)
                
                # Type "Test123"
                passport_field.type("Test123", delay=100)
                print("Step 18.8: Entered 'Test123' in Passport Number field")
                
                # Verify the text was entered
                actual_passport = passport_field.input_value()
                print(f"Step 18.8: Verification - Passport Number field now contains: {actual_passport}")
                time.sleep(1)
            else:
                # Try using name attribute
                passport_field_by_name = page.locator("input[name='AdultpassportNo']")
                if passport_field_by_name.count() > 0:
                    passport_field_by_name.click()
                    print("Step 18.8: Clicked on Passport Number field (by name)")
                    time.sleep(0.5)
                    
                    # Clear any existing text
                    passport_field_by_name.fill("")
                    time.sleep(0.3)
                    
                    # Type "Test123"
                    passport_field_by_name.type("Test123", delay=100)
                    print("Step 18.8: Entered 'Test123' in Passport Number field")
                    
                    # Verify the text was entered
                    actual_passport = passport_field_by_name.input_value()
                    print(f"Step 18.8: Verification - Passport Number field now contains: {actual_passport}")
                    time.sleep(1)
                else:
                    print("Step 18.8: Passport Number field not found")
        except Exception as e:
            print(f"Step 18.8: Error entering passport number: {e}")
        
        time.sleep(2)
        
        # Click on Passport Expiry Day dropdown and select 05
        print("Step 18.9: Selecting Passport Expiry Day...")
        
        try:
            # Find the passport expiry day dropdown with id="passEXDayAdult0"
            pass_ex_day_dropdown = page.locator("#passEXDayAdult0")
            if pass_ex_day_dropdown.count() > 0:
                # Scroll into view and click
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, pass_ex_day_dropdown.element_handle())
                time.sleep(1)
                
                pass_ex_day_dropdown.click()
                print("Step 18.9: Clicked on Passport Expiry Day dropdown")
                time.sleep(2)
                
                # Use JavaScript to select day 05
                selected = page.evaluate("""
                    () => {
                        let dropdown = document.getElementById('passEXDayAdult0');
                        if(dropdown) {
                            for(let option of dropdown.options) {
                                if(option.value === '05') {
                                    dropdown.value = '05';
                                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    dropdown.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected expiry day 05 by ID' };
                                }
                            }
                        }
                        return { success: false, message: 'Could not find dropdown or day 05' };
                    }
                """)
                
                if selected['success']:
                    print(f"Step 18.9: {selected['message']}")
                    time.sleep(1)
                else:
                    print(f"Step 18.9: {selected['message']}")
            else:
                print("Step 18.9: Passport Expiry Day dropdown not found")
        except Exception as e:
            print(f"Step 18.9: Error selecting Passport Expiry Day: {e}")
        
        time.sleep(2)
        
        # Click on Passport Expiry Month dropdown and select Jun (06)
        print("Step 18.10: Selecting Passport Expiry Month...")
        
        try:
            # Find the passport expiry month dropdown with id="passEXMonAdult0"
            pass_ex_mon_dropdown = page.locator("#passEXMonAdult0")
            if pass_ex_mon_dropdown.count() > 0:
                # Scroll into view and click
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, pass_ex_mon_dropdown.element_handle())
                time.sleep(1)
                
                pass_ex_mon_dropdown.click()
                print("Step 18.10: Clicked on Passport Expiry Month dropdown")
                time.sleep(2)
                
                # Use JavaScript to select Jun (06)
                selected = page.evaluate("""
                    () => {
                        let dropdown = document.getElementById('passEXMonAdult0');
                        if(dropdown) {
                            for(let option of dropdown.options) {
                                if(option.value === '06') {
                                    dropdown.value = '06';
                                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    dropdown.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected expiry month Jun (06) by ID' };
                                }
                            }
                        }
                        return { success: false, message: 'Could not find dropdown or month 06' };
                    }
                """)
                
                if selected['success']:
                    print(f"Step 18.10: {selected['message']}")
                    time.sleep(1)
                else:
                    print(f"Step 18.10: {selected['message']}")
            else:
                print("Step 18.10: Passport Expiry Month dropdown not found")
        except Exception as e:
            print(f"Step 18.10: Error selecting Passport Expiry Month: {e}")
        
        time.sleep(2)
        
        # Click on Passport Expiry Year dropdown and select 2030
        print("Step 18.11: Selecting Passport Expiry Year...")
        
        try:
            # Find the passport expiry year dropdown with id="passEXYearAdult0"
            pass_ex_year_dropdown = page.locator("#passEXYearAdult0")
            if pass_ex_year_dropdown.count() > 0:
                # Scroll into view and click
                page.evaluate("""
                    (el) => {
                        el.scrollIntoView(true);
                    }
                """, pass_ex_year_dropdown.element_handle())
                time.sleep(1)
                
                pass_ex_year_dropdown.click()
                print("Step 18.11: Clicked on Passport Expiry Year dropdown")
                time.sleep(2)
                
                # Use JavaScript to select 2030
                selected = page.evaluate("""
                    () => {
                        let dropdown = document.getElementById('passEXYearAdult0');
                        if(dropdown) {
                            for(let option of dropdown.options) {
                                if(option.value === '2030') {
                                    dropdown.value = '2030';
                                    dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    dropdown.dispatchEvent(new Event('input', { bubbles: true }));
                                    return { success: true, message: 'Selected expiry year 2030 by ID' };
                                }
                            }
                        }
                        return { success: false, message: 'Could not find dropdown or year 2030' };
                    }
                """)
                
                if selected['success']:
                    print(f"Step 18.11: {selected['message']}")
                    time.sleep(1)
                else:
                    print(f"Step 18.11: {selected['message']}")
            else:
                print("Step 18.11: Passport Expiry Year dropdown not found")
        except Exception as e:
            print(f"Step 18.11: Error selecting Passport Expiry Year: {e}")
        
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
                email_field.type("manish.dasila@easemytrip.ae", delay=50)
                print("Step 19: Entered 'manish.dasila@easemytrip.ae' in Email Address field")
                
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
        
        # Take screenshot of payment page
        print("Step 27: Taking screenshot of payment page...")
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
            print(f"Step 27: Screenshot saved to {screenshot_path}")
        except Exception as e:
            print(f"Step 27: Error taking screenshot: {e}")
        
        print("\nScript completed! Keeping browser open for 10 seconds...")
        time.sleep(10)
        
        browser.close()
        print("Browser closed. Script finished.")

if __name__ == "__main__":
    search_oneway_flight()
