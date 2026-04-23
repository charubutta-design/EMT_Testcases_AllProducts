from playwright.sync_api import sync_playwright
import sys
from time import sleep
from datetime import datetime, timedelta

def navigate_to_flights():
    with sync_playwright() as p:
        # Launch browser with maximized window
        browser = p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        # Create context with no viewport (uses full screen)
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        # Navigate to EaseMyTrip website
        print("Navigating to EaseMyTrip...")
        page.goto("https://www.easemytrip.com/", wait_until="domcontentloaded")
        
        # Handle location permission popup - click "Never allow" or close
        try:
            print("Handling location popup...")
            never_allow_btn = page.locator('text="Never allow"')
            if never_allow_btn.is_visible(timeout=1000):
                never_allow_btn.click()
                print("Closed location popup")
                page.wait_for_timeout(500)
        except:
            print("No location popup found or already closed")
        
        # Ensure we're on the Flights tab (it should be selected by default)
        try:
            # Look for the Flights tab in the navigation
            flights_tab = page.locator('text="Flights"')
            if flights_tab.is_visible(timeout=1000):
                flights_tab.click()
                print("Clicked on Flights tab")
                page.wait_for_timeout(1000)
        except:
            print("Flights section already active")
        
        # Click on 'Defence Forces' (class="container_df")
        try:
            print("Clicking on Defence Forces...")
            defence_forces = page.locator('label.container_df:has-text("Defence Forces")')
            if defence_forces.is_visible(timeout=2000):
                defence_forces.click()
                print("Successfully clicked on Defence Forces")
                page.wait_for_timeout(1000)
            else:
                print("Defence Forces element not found or not visible")
        except Exception as e:
            print(f"Error clicking on Defence Forces: {e}")
        
        # Click on the date input field and select a date 20 days from today
        try:
            print("Clicking on date input field...")
            date_input = page.locator('input.input_cld[id="ddate"]')
            if date_input.is_visible(timeout=2000):
                date_input.click()
                print("Clicked on date input field")
                page.wait_for_timeout(1500)
                
                # Calculate date 20 days from today
                target_date = datetime.now() + timedelta(days=20)
                formatted_date = target_date.strftime('%d/%m/%Y')
                day = target_date.day
                
                print(f"Setting date to: {formatted_date} (day: {day})")
                
                # Method 1: Try to click on the date in the calendar swiper
                try:
                    # Look for the day in the swiper carousel
                    day_element = page.locator(f'.swiper-slide').filter(has_text=str(day)).first
                    
                    if day_element.is_visible(timeout=1000):
                        # Get bounding box to ensure it's the actual calendar
                        bbox = day_element.bounding_box()
                        if bbox and 100 < bbox['y'] < 600:  # Should be in reasonable calendar area
                            day_element.click()
                            print(f"✓ Clicked on date: {day}")
                            page.wait_for_timeout(1000)
                            
                            # Verify
                            final_value = date_input.input_value()
                            print(f"Date field value: {final_value}")
                except Exception as e:
                    print(f"Calendar click attempt failed: {e}")
                
                # Method 2: Use fill() method which might work better
                try:
                    print("Attempting to fill date field...")
                    date_input.fill(formatted_date)
                    page.wait_for_timeout(500)
                    final_value = date_input.input_value()
                    print(f"Date field value after fill: {final_value}")
                except Exception as e:
                    print(f"Fill attempt failed: {e}")
                    
            else:
                print("Date input field not found or not visible")
        except Exception as e:
            print(f"Error in date selection: {e}")
        
        # Click on the Search button
        try:
            print("Clicking on Search button...")
            
            search_btn = page.locator('[class="srchBtnSe"]')
            
            if search_btn.count() > 0:
                # Remove the overlay that blocks clicking
                page.evaluate("document.getElementById('overlaybg1')?.remove()")
                page.wait_for_timeout(300)
                
                # Now click the button
                search_btn.first.click()
                print("✓ Successfully clicked on Search button")
                page.wait_for_timeout(8000)
                
        except Exception as e:
            print(f"Error clicking Search button: {e}")
        
        # Wait for listing page to load and click on Air India Express checkbox
        try:
            print("Waiting for listing page to load...")
            # Wait for the filter section to appear
            page.wait_for_selector('label:has-text("Air India Express")', timeout=20000)
            print("✓ Listing page loaded - found Air India Express option")
            page.wait_for_timeout(2000)
            
            # Look for Air India Express within the Airlines filter
            air_india_express = page.locator('label:has-text("Air India Express")').first
            
            if air_india_express.is_visible(timeout=2000):
                print("Air India Express option is visible")
                
                # Find the associated checkbox within the label
                checkbox = air_india_express.locator('.checkmark_lgn')
                
                if checkbox.count() > 0:
                    checkbox.click()
                    print("✓ Successfully clicked on Air India Express checkbox")
                    page.wait_for_timeout(2000)
                else:
                    # Try clicking the label directly
                    air_india_express.click()
                    print("✓ Clicked on Air India Express label")
                    page.wait_for_timeout(2000)
            else:
                print("Air India Express option not visible")
                
        except Exception as e:
            print(f"Error selecting Air India Express: {e}")
        
        # Click on 'Book Now' button
        try:
            print("Looking for Book Now button...")
            page.wait_for_timeout(2000)
            
            # Find the Book Now button - it could be a button or link
            book_now_btn = page.locator('button:has-text("Book Now"), a:has-text("Book Now"), [value="Book Now"]').first
            
            if book_now_btn.is_visible(timeout=3000):
                print("Found Book Now button")
                book_now_btn.click()
                print("✓ Successfully clicked on Book Now button")
                page.wait_for_timeout(3000)
            else:
                print("Book Now button not found or not visible")
                # Take screenshot to debug
                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\book_now_debug.png")
                print("Debug screenshot saved")
                
        except Exception as e:
            print(f"Error clicking Book Now button: {e}")
        
        # Find and select 'ArmedForces' fare and click the Book Now button
        try:
            print("Looking for ArmedForces fare option...")
            page.wait_for_timeout(2000)
            
            # Find the ArmedForces option
            armed_forces_label = page.locator('label:has-text("ArmedForces")').first
            
            if armed_forces_label.is_visible(timeout=3000):
                print("✓ Found ArmedForces label")
                
                # Scroll into view
                armed_forces_label.scroll_into_view_if_needed()
                page.wait_for_timeout(500)
                
                # Find the parent container - try multiple class names
                parent_container = armed_forces_label.locator('xpath=./ancestor::div[contains(@class, "flightOpt") or contains(@class, "flight-option") or contains(@class, "fare-option") or contains(@class, "option-row") or contains(@class, "flight-result")]').first
                
                if parent_container.count() == 0:
                    # If not found, get the closest parent with significant width/padding
                    parent_container = armed_forces_label.locator('xpath=./ancestor::div[self::div[contains(@style, "display")]]').first
                
                if parent_container.count() == 0:
                    # Last resort - get the grandparent
                    parent_container = armed_forces_label.locator('xpath=./ancestor::div[2]').first
                
                print(f"Parent container found: {parent_container.count() > 0}")
                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\armed_forces_parent.png")
                
                if parent_container.count() > 0:
                    # Click the radio button
                    radio = armed_forces_label.locator('input[type="radio"]').first
                    if radio.count() == 0:
                        radio = armed_forces_label.locator('xpath=./preceding-sibling::input[@type="radio"]').first
                    
                    if radio.count() > 0:
                        try:
                            radio.click()
                            print("✓ Clicked ArmedForces radio button")
                            page.wait_for_timeout(1000)
                        except Exception as e:
                            print(f"Could not click radio: {e}")
                    
                    # Find all potential Book Now buttons in parent
                    all_buttons = parent_container.locator('button, a, input[type="button"], input[type="submit"]')
                    print(f"Found {all_buttons.count()} button elements")
                    
                    # Look for Book Now button
                    book_button_found = False
                    for i in range(min(10, all_buttons.count())):  # Check first 10 buttons
                        btn = all_buttons.nth(i)
                        try:
                            btn_text = btn.text_content() or btn.get_attribute('value') or btn.get_attribute('title') or ''
                            print(f"Button {i}: '{btn_text}'")
                            
                            if 'book' in btn_text.lower() and 'now' in btn_text.lower():
                                print(f"✓ Found Book Now button at index {i}")
                                btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                # Take screenshot before clicking
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\before_armed_forces_book_now.png")
                                print("Screenshot saved: before_armed_forces_book_now.png")
                                btn.click()
                                print("✓ Successfully clicked Book Now for ArmedForces fare")
                                page.wait_for_timeout(3000)
                                book_button_found = True
                                break
                        except Exception as e:
                            print(f"Error checking button {i}: {e}")
                    
                    if book_button_found:
                        current_url = page.url
                        print(f"Navigated to: {current_url}")
                        
                        # Wait for the booking page to load
                        page.wait_for_timeout(2000)
                        
                        # Select title for adult passenger
                        try:
                            print("Selecting title for adult passenger...")
                            
                            # Find the title dropdown
                            title_dropdown = page.locator('select[name="TitleAdult"][id="titleAdult0"]').first
                            
                            if title_dropdown.is_visible(timeout=3000):
                                print("✓ Found title dropdown")
                                
                                # Use select_option method which doesn't require the option to be visible
                                title_dropdown.select_option(value="Mr")
                                print("✓ Successfully selected 'Mr' from title dropdown")
                                page.wait_for_timeout(500)
                            else:
                                print("✗ Title dropdown not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\title_dropdown_not_found.png")
                                
                        except Exception as e:
                            print(f"Error selecting title: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Enter first name
                        try:
                            print("Entering first name...")
                            
                            first_name_input = page.locator('input[id="txtFNAdult0"]').first
                            
                            if first_name_input.is_visible(timeout=3000):
                                print("✓ Found first name input field")
                                first_name_input.click()
                                page.wait_for_timeout(300)
                                
                                # Clear any existing text and enter "Manni"
                                first_name_input.fill("Manni")
                                print("✓ Successfully entered 'Manni' in first name field")
                                page.wait_for_timeout(500)
                            else:
                                print("✗ First name input field not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\first_name_not_found.png")
                                
                        except Exception as e:
                            print(f"Error entering first name: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Enter last name
                        try:
                            print("Entering last name...")
                            
                            last_name_input = page.locator('input[id="txtLNAdult0"]').first
                            
                            if last_name_input.is_visible(timeout=3000):
                                print("✓ Found last name input field")
                                last_name_input.click()
                                page.wait_for_timeout(300)
                                
                                # Clear any existing text and enter "Test"
                                last_name_input.fill("Test")
                                print("✓ Successfully entered 'Test' in last name field")
                                page.wait_for_timeout(500)
                            else:
                                print("✗ Last name input field not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\last_name_not_found.png")
                                
                        except Exception as e:
                            print(f"Error entering last name: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Enter service ID with conditional logic
                        try:
                            print("Looking for service ID field...")
                            
                            # Take a screenshot before searching
                            page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\before_service_id_search.png")
                            print("Screenshot saved: before_service_id_search.png")
                            
                            # Try different selectors to find the element
                            # Method 1: Find by ID (without tag restriction)
                            service_id_field = page.locator('#divServiceIDAdult0').first
                            
                            # Method 2: If not found, try with div tag
                            if service_id_field.count() == 0:
                                service_id_field = page.locator('div#divServiceIDAdult0').first
                            
                            # Method 3: If still not found, look for any element with that ID
                            if service_id_field.count() == 0:
                                service_id_field = page.locator('[id="divServiceIDAdult0"]').first
                            
                            # Method 4: Look for input inside the div
                            if service_id_field.count() == 0:
                                service_id_field = page.locator('#divServiceIDAdult0 input').first
                            
                            print(f"Service ID field found: {service_id_field.count() > 0}")
                            
                            if service_id_field.count() > 0:
                                print("✓ Found service ID field (id='divServiceIDAdult0')")
                                
                                # Scroll into view
                                service_id_field.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # Click on the field
                                service_id_field.click()
                                page.wait_for_timeout(300)
                                
                                # Enter the service ID
                                service_id_field.fill("123ABC")
                                print("✓ Successfully entered '123ABC' in service ID field")
                                page.wait_for_timeout(500)
                            else:
                                print("✗ FAILED: Service ID field (id='divServiceIDAdult0') not found")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\service_id_not_found.png")
                                print("Debug screenshot saved: service_id_not_found.png")
                                # Fail the test case
                                raise Exception("Test Case FAILED: Required element 'divServiceIDAdult0' not found on the page")
                                
                        except Exception as e:
                            if "Test Case FAILED" in str(e):
                                print(f"✗ TEST FAILED: {e}")
                                sys.exit(1)
                            else:
                                print(f"Error entering service ID: {e}")
                                import traceback
                                traceback.print_exc()
                                sys.exit(1)
                        
                        # Enter email address
                        try:
                            print("Entering email address...")
                            
                            email_input = page.locator('input[id="txtEmailId"][name="trvLoginEmail2"]').first
                            
                            if email_input.is_visible(timeout=3000):
                                print("✓ Found email input field")
                                email_input.click()
                                page.wait_for_timeout(300)
                                
                                # Clear any existing text and enter the email
                                email_input.fill("manish.dasila@easemytrip.com")
                                print("✓ Successfully entered 'manish.dasila@easemytrip.com' in email field")
                                page.wait_for_timeout(500)
                            else:
                                print("✗ Email input field not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\email_not_found.png")
                                
                        except Exception as e:
                            print(f"Error entering email: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Enter mobile phone number
                        try:
                            print("Entering mobile phone number...")
                            
                            phone_input = page.locator('input[id="txtCPhone"][placeholder="Enter Mobile no."]').first
                            
                            if phone_input.is_visible(timeout=3000):
                                print("✓ Found mobile phone input field")
                                phone_input.click()
                                page.wait_for_timeout(300)
                                
                                # Clear any existing text and enter the phone number
                                phone_input.fill("9999999999")
                                print("✓ Successfully entered '9999999999' in mobile phone field")
                                page.wait_for_timeout(500)
                            else:
                                print("✗ Mobile phone input field not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\phone_not_found.png")
                                
                        except Exception as e:
                            print(f"Error entering mobile phone: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on ACKO insurance radio button
                        try:
                            print("Looking for ACKO insurance radio button...")
                            
                            # Wait for the insurance section to load
                            page.wait_for_timeout(2000)
                            
                            # Take screenshot before looking for insurance
                            page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\before_insurance_search.png")
                            print("Screenshot saved: before_insurance_search.png")
                            
                            # Try different selectors
                            # Method 1: By class name on input
                            insurance_btn = page.locator('input.insur-yes').first
                            
                            # Method 2: If not found, look for any element with insur-yes class
                            if insurance_btn.count() == 0:
                                insurance_btn = page.locator('.insur-yes').first
                            
                            # Method 3: Look for radio button with insur-yes in parent
                            if insurance_btn.count() == 0:
                                insurance_btn = page.locator('[class*="insur-yes"]').first
                            
                            print(f"Insurance button found: {insurance_btn.count() > 0}")
                            
                            if insurance_btn.count() > 0 and insurance_btn.is_visible(timeout=3000):
                                print("✓ Found ACKO insurance radio button (class='insur-yes')")
                                insurance_btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # Click the radio button
                                insurance_btn.click()
                                print("✓ Successfully clicked ACKO insurance radio button")
                                page.wait_for_timeout(1000)
                            else:
                                print("✗ ACKO insurance radio button not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\insurance_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking ACKO insurance button: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on Continue Booking button
                        try:
                            print("Looking for Continue Booking button...")
                            
                            continue_btn = page.locator('#spnTransaction').first
                            
                            if continue_btn.is_visible(timeout=3000):
                                print("✓ Found Continue Booking button (id='spnTransaction')")
                                continue_btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # Click the button
                                continue_btn.click()
                                print("✓ Successfully clicked Continue Booking button")
                                page.wait_for_timeout(3000)
                                
                                # Check the new URL
                                current_url = page.url
                                print(f"Navigated to: {current_url}")
                            else:
                                print("✗ Continue Booking button not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\continue_booking_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking Continue Booking button: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on 'Secure My Trip' button in Free Cancellation popup
                        try:
                            print("Looking for 'Secure My Trip' button...")
                            
                            # Wait for the popup to appear with better load state handling
                            page.wait_for_timeout(3000)
                            try:
                                page.wait_for_load_state('networkidle', timeout=5000)
                            except:
                                pass  # Continue if networkidle times out
                            
                            # Take screenshot before searching
                            page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\before_secure_trip_search.png")
                            print("Screenshot saved: before_secure_trip_search.png")
                            
                            # Find the Secure My Trip button
                            secure_btn = page.locator('button.conf_btn').first
                            
                            # If not found as button, try as any element with that class
                            if secure_btn.count() == 0:
                                secure_btn = page.locator('.conf_btn').first
                            
                            # Try finding by text
                            if secure_btn.count() == 0:
                                secure_btn = page.locator("button, div").filter(has_text="Secure My Trip").first
                            
                            print(f"Secure My Trip button count: {secure_btn.count()}")
                            
                            if secure_btn.count() > 0:
                                try:
                                    is_visible = secure_btn.is_visible(timeout=3000)
                                    if is_visible:
                                        print("✓ Found 'Secure My Trip' button (class='conf_btn')")
                                        secure_btn.scroll_into_view_if_needed()
                                        page.wait_for_timeout(300)
                                        
                                        # Click the button
                                        secure_btn.click()
                                        print("✓ Successfully clicked 'Secure My Trip' button")
                                        page.wait_for_timeout(3000)
                                        
                                        # Check the new URL
                                        current_url = page.url
                                        print(f"Navigated to: {current_url}")
                                    else:
                                        print("✗ Button found but not visible, trying with force=True...")
                                        secure_btn.scroll_into_view_if_needed()
                                        page.wait_for_timeout(500)
                                        
                                        # Try with force click
                                        secure_btn.click(force=True)
                                        print("✓ Force-clicked 'Secure My Trip' button")
                                        page.wait_for_timeout(3000)
                                        
                                        current_url = page.url
                                        print(f"Navigated to: {current_url}")
                                except Exception as ve:
                                    print(f"Error: {ve}, trying force click...")
                                    try:
                                        secure_btn.click(force=True)
                                        print("✓ Force-clicked 'Secure My Trip' button")
                                        page.wait_for_timeout(3000)
                                    except:
                                        page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\secure_trip_click_failed.png")
                            else:
                                print("✗ 'Secure My Trip' button not found")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\secure_trip_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking 'Secure My Trip' button: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on 'Skip' button in seat selection popup
                        try:
                            print("Looking for 'Skip' button in seat selection popup...")
                            
                            # Wait for the popup to appear
                            page.wait_for_timeout(2000)
                            
                            # Find the Skip button
                            skip_btn = page.locator('button.skipbtn').first
                            
                            # If not found as button, try as any element with that class
                            if skip_btn.count() == 0:
                                skip_btn = page.locator('.skipbtn').first
                            
                            if skip_btn.count() > 0 and skip_btn.is_visible(timeout=3000):
                                print("✓ Found 'Skip' button (class='skipbtn')")
                                skip_btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # Click the button
                                skip_btn.click()
                                print("✓ Successfully clicked 'Skip' button")
                                page.wait_for_timeout(3000)
                                
                                # Check the new URL
                                current_url = page.url
                                print(f"Navigated to: {current_url}")
                            else:
                                print("✗ 'Skip' button not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\skip_btn_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking 'Skip' button: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on 'Skip to Payment' button
                        try:
                            print("Looking for 'Skip to Payment' button...")
                            
                            # Wait for the button to appear
                            page.wait_for_timeout(2000)
                            
                            # Find the Skip to Payment button
                            skip_payment_btn = page.locator('button.skipotp').first
                            
                            # If not found, try with the full class name
                            if skip_payment_btn.count() == 0:
                                skip_payment_btn = page.locator('.skipotp.ng-star-inserted').first
                            
                            # If still not found, try as any element with skipotp class
                            if skip_payment_btn.count() == 0:
                                skip_payment_btn = page.locator('[class*="skipotp"]').first
                            
                            if skip_payment_btn.count() > 0 and skip_payment_btn.is_visible(timeout=3000):
                                print("✓ Found 'Skip to Payment' button (class='skipotp ng-star-inserted')")
                                skip_payment_btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # Click the button
                                skip_payment_btn.click()
                                print("✓ Successfully clicked 'Skip to Payment' button")
                                page.wait_for_timeout(3000)
                                
                                # Check the new URL
                                current_url = page.url
                                print(f"Navigated to: {current_url}")
                            else:
                                print("✗ 'Skip to Payment' button not found or not visible")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\skip_payment_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking 'Skip to Payment' button: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on 'Wallets' payment option
                        try:
                            print("Looking for 'Wallets' payment option...")
                            
                            # Wait for the payment page to load
                            page.wait_for_timeout(3000)
                            
                            # Take screenshot to see the checkout page
                            page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\checkout_page.png")
                            print("Screenshot saved: checkout_page.png")
                            
                            # Get all available payment options
                            all_elements = page.locator("button, div[class*='wallet'], div[class*='payment']").all()
                            print(f"Total payment elements found: {len(all_elements)}")
                            
                            # Find the Wallets button with multiple methods
                            wallets_btn = page.locator('button.wallet-txt.PG2').first
                            
                            # If not found as button, try as any element with wallet-txt class
                            if wallets_btn.count() == 0:
                                wallets_btn = page.locator('.wallet-txt.PG2').first
                            
                            # If still not found, try with just wallet-txt class
                            if wallets_btn.count() == 0:
                                wallets_btn = page.locator('.wallet-txt').first
                            
                            # Try finding by text content
                            if wallets_btn.count() == 0:
                                wallets_btn = page.locator("button, div").filter(has_text="Wallet").first
                            
                            print(f"Wallets button count: {wallets_btn.count()}")
                            
                            if wallets_btn.count() > 0:
                                is_visible = False
                                try:
                                    is_visible = wallets_btn.is_visible(timeout=2000)
                                except:
                                    pass
                                print(f"Wallets button visible: {is_visible}")
                                
                                if is_visible:
                                    print("✓ Found 'Wallets' payment option (class='wallet-txt PG2')")
                                    wallets_btn.scroll_into_view_if_needed()
                                    page.wait_for_timeout(300)
                                    
                                    # Click the Wallets button
                                    wallets_btn.click()
                                    print("✓ Successfully clicked 'Wallets' payment option")
                                    page.wait_for_timeout(2000)
                                    
                                    # Check the current page
                                    current_url = page.url
                                    print(f"Current page: {current_url}")
                                else:
                                    print("✗ 'Wallets' button found but not visible, using force click...")
                                    wallets_btn.scroll_into_view_if_needed()
                                    page.wait_for_timeout(300)
                                    wallets_btn.click(force=True)
                                    print("✓ Force-clicked 'Wallets' payment option")
                                    page.wait_for_timeout(2000)
                                    
                                    current_url = page.url
                                    print(f"Current page: {current_url}")
                            else:
                                print("✗ 'Wallets' payment option not found")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\wallets_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking 'Wallets' payment option: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on 'Bajaj Pay' radio button
                        try:
                            print("Looking for 'Bajaj Pay' radio button...")
                            
                            # Wait for the Wallets options to load
                            page.wait_for_timeout(2000)
                            
                            # Take screenshot before searching
                            page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\before_bajaj_search.png")
                            print("Screenshot saved: before_bajaj_search.png")
                            
                            # Try different selectors
                            # Method 1: By ID attribute
                            bajaj_pay_btn = page.locator('[id="rdoBajaj Pay"]').first
                            
                            # Method 2: Try with space in attribute
                            if bajaj_pay_btn.count() == 0:
                                bajaj_pay_btn = page.locator('input[id*="Bajaj"]').first
                            
                            # Method 3: By class name
                            if bajaj_pay_btn.count() == 0:
                                bajaj_pay_btn = page.locator('input.checkmark_ntb').first
                            
                            # Method 4: Try finding by label text
                            if bajaj_pay_btn.count() == 0:
                                bajaj_pay_label = page.locator('text="Bajaj Pay"').first
                                if bajaj_pay_label.count() > 0:
                                    bajaj_pay_btn = bajaj_pay_label.locator('xpath=./preceding-sibling::input[@type="radio"]').first
                            
                            print(f"Bajaj Pay button found: {bajaj_pay_btn.count() > 0}")
                            
                            if bajaj_pay_btn.count() > 0:
                                print("✓ Found 'Bajaj Pay' radio button")
                                
                                # Try to click directly
                                try:
                                    bajaj_pay_btn.click(force=True)
                                    print("✓ Successfully clicked 'Bajaj Pay' radio button")
                                except:
                                    # Try JavaScript click if regular click fails
                                    print("Regular click failed, trying JavaScript click...")
                                    element_handle = bajaj_pay_btn.element_handle()
                                    page.evaluate("(el) => el.click()", element_handle)
                                    print("✓ JavaScript click successful")
                                
                                page.wait_for_timeout(1500)
                                
                                # Check the current page
                                current_url = page.url
                                print(f"Current page: {current_url}")
                            else:
                                print("✗ 'Bajaj Pay' radio button not found")
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\bajaj_pay_not_found.png")
                                
                        except Exception as e:
                            print(f"Error clicking 'Bajaj Pay' radio button: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Click on 'Make Payment' button
                        try:
                            print("Looking for 'Make Payment' button...")
                            
                            # Wait for the button to appear
                            page.wait_for_timeout(2000)
                            
                            # STEP 1: Capture amount from checkout page before Make Payment
                            print("\n=== Capturing Amount on Checkout Page ===")
                            amount_before = None
                            
                            # Try multiple selectors to find the amount
                            amount_selectors = [
                                '.total-price',
                                '[class*="total"]',
                                '[class*="amount"]',
                                '[class*="price"]',
                                'div:has-text("₹")',
                                '.grand-total',
                                '[id*="total"]'
                            ]
                            
                            for selector in amount_selectors:
                                try:
                                    elements = page.locator(selector).all()
                                    if elements:
                                        for elem in elements:
                                            text = elem.text_content().strip()
                                            if '₹' in text or text.replace(',', '').replace('.', '').isdigit():
                                                amount_before = text
                                                print(f"✓ Found amount on checkout page: {amount_before}")
                                                break
                                        if amount_before:
                                            break
                                except:
                                    pass
                            
                            if not amount_before:
                                print("⚠ WARNING: Could not find amount on checkout page")
                            else:
                                print(f"Amount before Make Payment: {amount_before}")
                            
                            # Find the Make Payment button
                            make_payment_btn = page.locator('button.mk-pym4').first
                            
                            # If not found as button, try as any element with that class
                            if make_payment_btn.count() == 0:
                                make_payment_btn = page.locator('.mk-pym4').first
                            
                            if make_payment_btn.count() > 0 and make_payment_btn.is_visible(timeout=3000):
                                print("✓ Found 'Make Payment' button (class='mk-pym4')")
                                make_payment_btn.scroll_into_view_if_needed()
                                page.wait_for_timeout(300)
                                
                                # Click the Make Payment button
                                make_payment_btn.click()
                                print("✓ Successfully clicked 'Make Payment' button")
                                page.wait_for_timeout(3000)
                                
                                # Check the current page
                                current_url = page.url
                                print(f"Navigated to: {current_url}")
                                
                                # Take screenshot of payment gateway page
                                page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\payment_gateway_page.png")
                                print("Screenshot saved: payment_gateway_page.png")
                                
                                # Wait for page to load
                                page.wait_for_timeout(3000)
                                
                                # STEP 2: Capture amount from payment gateway page after Make Payment
                                print("\n=== Capturing Amount on Payment Gateway Page ===")
                                amount_after = None
                                page_content = page.content()
                                
                                # Try multiple selectors to find the amount on payment gateway
                                payment_amount_selectors = [
                                    '.amtrow',  # Primary selector from TPSL gateway
                                    'label.amtrow',
                                    'text/Amount : ',
                                    '[class*="amount"]',
                                    '[class*="total"]',
                                    '[class*="price"]',
                                    '[class*="txn"]',
                                    '[class*="value"]',
                                    'div:has-text("Amount")',
                                    'label:has-text("Amount")',
                                    '.txn-amount',
                                    '[id*="amount"]'
                                ]
                                
                                for selector in payment_amount_selectors:
                                    try:
                                        elements = page.locator(selector).all()
                                        if elements:
                                            for elem in elements:
                                                text = elem.text_content().strip()
                                                # Look for amount patterns:
                                                # 1. Contains rupee symbol
                                                # 2. Is numeric with . or ,
                                                # 3. Contains "Amount" text with number
                                                if '₹' in text:
                                                    amount_after = text
                                                    print(f"✓ Found amount on payment gateway: {amount_after}")
                                                    break
                                                elif 'Amount' in text and ':' in text:
                                                    # Extract number from "Amount : 7901.00" format
                                                    import re
                                                    match = re.search(r'[\d,]+\.?\d*', text)
                                                    if match:
                                                        amount_after = match.group()
                                                        print(f"✓ Found amount on payment gateway: {amount_after} (from text: {text})")
                                                        break
                                                elif text.replace(',', '').replace('.', '').isdigit() and len(text) > 0:
                                                    amount_after = text
                                                    print(f"✓ Found amount on payment gateway: {amount_after}")
                                                    break
                                            if amount_after:
                                                break
                                    except:
                                        pass
                                
                                if not amount_after:
                                    print("⚠ WARNING: Could not find amount on payment gateway page")
                                    # Try regex extraction from page content
                                    import re
                                    rupee_pattern = r'₹\s*[\d,.]+'
                                    matches = re.findall(rupee_pattern, page_content)
                                    if matches:
                                        amount_after = matches[0]
                                        print(f"✓ Found amount via regex: {amount_after}")
                                    else:
                                        # Save HTML for debugging
                                        with open("D:\\EMT_Flight_Playwright\\Test_cases\\payment_gateway_html.txt", "w", encoding='utf-8') as f:
                                            f.write(page_content)
                                        print("⚠ Saved payment gateway HTML to payment_gateway_html.txt for analysis")
                                else:
                                    print(f"Amount after Make Payment: {amount_after}")
                                
                                # STEP 3: Validate amounts match
                                print("\n=== Validating Amount Match ===")
                                if amount_before and amount_after:
                                    # Normalize amounts for comparison
                                    # Remove rupee symbol, commas, spaces, and normalize decimals
                                    import re
                                    
                                    def normalize_amount(amount_str):
                                        # Remove rupee symbol, commas, spaces
                                        cleaned = amount_str.replace('₹', '').replace(',', '').replace(' ', '').strip()
                                        # Extract numeric parts
                                        match = re.search(r'(\d+)\.?(\d*)', cleaned)
                                        if match:
                                            whole = match.group(1)
                                            decimal = match.group(2) or ''
                                            # If decimal exists and is not just zeros, keep it; otherwise return whole number
                                            if decimal and int(decimal) != 0:
                                                return f"{whole}.{decimal}"
                                            else:
                                                return whole
                                        return cleaned
                                    
                                    amount_before_normalized = normalize_amount(amount_before)
                                    amount_after_normalized = normalize_amount(amount_after)
                                    
                                    print(f"Checkout amount (normalized): {amount_before_normalized}")
                                    print(f"Payment gateway amount (normalized): {amount_after_normalized}")
                                    
                                    if amount_before_normalized == amount_after_normalized:
                                        print("✓✓✓ VALIDATION PASSED: Amounts match!")
                                        print(f"    Checkout: {amount_before}")
                                        print(f"    Payment Gateway: {amount_after}")
                                    else:
                                        print("✗✗✗ VALIDATION FAILED: Amounts do NOT match!")
                                        print(f"    Checkout: {amount_before}")
                                        print(f"    Payment Gateway: {amount_after}")
                                        page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\amount_mismatch.png")
                                        raise AssertionError(f"Amount mismatch: Checkout={amount_before}, Payment Gateway={amount_after}")
                                else:
                                    print("⚠ Could not validate amounts - one or both amounts not found")
                                    if not amount_before:
                                        print("  Missing: Amount on checkout page")
                                    if not amount_after:
                                        print("  Missing: Amount on payment gateway page")
                        except Exception as e:
                            print(f"Error clicking 'Make Payment' button: {e}")
                            import traceback
                            traceback.print_exc()
                    else:
                        print("✗ Book Now button not found")
                        page.screenshot(path="D:\\EMT_Flight_Playwright\\Test_cases\\ScreenShot\\no_book_button.png")
            else:
                print("✗ ArmedForces label not visible")
                
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
        
        print("Script completed. Closing browser...")
        sleep(2)
        browser.close()
        print("Browser closed.")

if __name__ == "__main__":
    navigate_to_flights()
