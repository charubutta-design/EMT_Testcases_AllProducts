from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta

def search_flight():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.easemytrip.com/")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)
        
        print("\n=== FLIGHT SEARCH AUTOMATION ===\n")
        
        # Step 1: Click From field and select New Delhi
        try:
            page.locator("#FromSector_show").click(force=True)
            print("✓ From field clicked")
            page.wait_for_timeout(500)
            page.type("#pff", "New Delhi", delay=50)
            page.wait_for_timeout(600)
            page.locator("li").filter(has_text="New Delhi").first.click()
            print("✓ From: New Delhi selected")
        except Exception as e:
            print(f"✗ From field error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(600)
        
        # Step 2: Click To field and select BOM
        try:
            page.type("input[placeholder='Destination City']", "BOM", delay=50)
            print("✓ To field: BOM typed")
            page.wait_for_timeout(600)
            page.locator("li").filter(has_text="Chhatrapati Shivaji").first.click(timeout=2000)
            print("✓ To: BOM selected")
        except Exception as e:
            print(f"✗ To field error: {e}")
            browser.close()
            return
        
        page.wait_for_timeout(800)
        
        # Step 3: Select date - 10 days from today
        target_date = datetime.now() + timedelta(days=10)
        date_str = target_date.strftime("%d/%m/%Y")
        print(f"✓ Departure Date: {date_str} (10 days from today)")
        
        try:
            # Find and fill date field
            date_field = page.locator("input[id*='ddate']").first
            date_field.fill(date_str)
            date_field.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
            print(f"✓ Departure date set to: {date_str}")
        except Exception as e:
            print(f"✗ Date selection error: {e}")
        
        page.wait_for_timeout(800)
        
        # Step 3b: Click on return date field first, then select return date - 3 days after departure date
        return_date = target_date + timedelta(days=3)
        return_date_str = return_date.strftime("%d/%m/%Y")
        print(f"✓ Return Date: {return_date_str} (3 days after departure)")
        
        try:
            # Remove overlay if present
            page.evaluate("""
            () => {
                let overlay = document.getElementById('overlaybg1');
                if (overlay) overlay.remove();
            }
            """)
            
            # Click on the return date field to open it
            return_date_fields = page.locator("input[id*='rdate']").all()
            if return_date_fields:
                return_date_field = return_date_fields[0]
                return_date_field.click(force=True)
                print("✓ Return date field clicked")
                page.wait_for_timeout(800)
                
                # Now fill the field and trigger events
                return_date_field.fill(return_date_str)
                return_date_field.evaluate(f"""
                el => {{
                    el.value = '{return_date_str}';
                    el.setAttribute('value', '{return_date_str}');
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                """)
                print(f"✓ Return date set to: {return_date_str}")
            else:
                print("⚠ Return date field not found")
        except Exception as e:
            print(f"✗ Return date selection error: {e}")
        
        page.wait_for_timeout(600)
        
        # Close calendar and blur focused element
        try:
            page.press("body", "Escape")
            page.evaluate("() => { if (document.activeElement && document.activeElement.blur) document.activeElement.blur(); }")
        except Exception as e:
            pass
        
        # Step 4: Click on Traveller & Class field
        print("✓ Clicking on Traveller & Class field...")
        try:
            # Remove overlay if present
            page.evaluate("() => { let overlay = document.getElementById('overlaybg1'); if (overlay) overlay.remove(); }")
            page.locator("#ptravlr").click(force=True)
            print("✓ Traveller & Class field clicked")
            page.wait_for_timeout(1000)
        except Exception as e:
            print(f"✗ Traveller & Class click error: {e}")
        
        page.wait_for_timeout(800)
        
        # Step 4b: Add one child
        print("✓ Adding one child...")
        try:
            page.evaluate("() => { let btn = document.getElementById('addchd'); if (btn) btn.click(); }")
            print("✓ Child added successfully via JavaScript")
            page.wait_for_timeout(800)
        except Exception as e:
            print(f"✗ Add child error: {e}")
        
        page.wait_for_timeout(600)
        
        # Step 4c: Add one infant
        print("✓ Adding one infant...")
        try:
            page.evaluate("() => { let btn = document.querySelector('.add.plus_box1Inf'); if (btn) btn.click(); }")
            print("✓ Infant added successfully via JavaScript")
            page.wait_for_timeout(600)
        except Exception as e:
            print(f"✗ Add infant error: {e}")
        
        page.wait_for_timeout(600)
        
        # Step 4d: Click Done button in Traveller & Class modal
        print("✓ Clicking Done button...")
        try:
            page.locator("#traveLer").click(timeout=3000, force=True)
            print("✓ Done button CLICKED!")
        except Exception as e:
            print(f"⚠ Direct click failed: {str(e)[:100]}")
            try:
                page.evaluate("() => { let doneBtn = document.getElementById('traveLer'); if (doneBtn) doneBtn.click(); }")
                print("✓ Done button clicked via JavaScript!")
            except Exception as e2:
                print(f"⚠ JavaScript click failed: {str(e2)[:100]}")
        
        page.wait_for_timeout(800)
        
        button_ready = page.evaluate("""
        () => {
            let checkButton = () => {
                let btn = document.querySelector('button.srchBtnSe');
                if (btn && btn.offsetWidth > 0 && btn.offsetHeight > 0) {
                    return true;
                }
                return false;
            };
            
            // Wait up to 10 seconds for button to be visible
            let timeout = 10000;
            let start = Date.now();
            while (Date.now() - start < timeout) {
                if (checkButton()) return true;
                // Spin wait (not ideal but simple)
            }
            return false;
        }
        """)
        
        if button_ready:
            print("✓ Search button is ready!")
        else:
            print("⚠ Button timeout - attempting anyway...")
        
        page.wait_for_timeout(600)
        
        # Step 6: Click Continue button first, then Search button
        print("\n🔍 STEP 1: Clicking Continue button (btn-refer.btn-block)...\n")
        
        try:
            page.evaluate("""
            () => {
                let btn = document.querySelector('button.btn-refer.btn-block');
                if (btn) {
                    btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    btn.click();
                }
            }
            """)
            print("✓ Continue button clicked via JavaScript")
        except Exception as e:
            print(f"⚠ Continue click error: {e}")
        
        page.wait_for_timeout(1000)
        
        print(f"📍 URL after Continue: {page.url}\n")
        
        print("🔍 STEP 2: Clicking Search Input (INPUT.srchBtnSe inside divSearchFlight)...\n")
        
        # Find input inside divSearchFlight
        btn_info = page.evaluate("""
        () => {
            let container = document.getElementById('divSearchFlight');
            if (container) {
                let input = container.querySelector('input.srchBtnSe');
                if (input) {
                    return {
                        found: true,
                        type: input.type,
                        className: input.className,
                        id: input.id,
                        value: input.value
                    };
                }
            }
            return { found: false };
        }
        """)
        print(f"📌 Search Input Info: {btn_info}\n")
        
        # Try Playwright click first
        try:
            print("Attempting Playwright click on input#divSearchFlight input.srchBtnSe...")
            page.locator("#divSearchFlight input.srchBtnSe").click(timeout=5000, force=True)
            print("✓ Search input clicked via Playwright")
        except Exception as e:
            print(f"⚠ Playwright click failed: {e}")
            
            # Fallback to JavaScript click
            try:
                page.evaluate("""
                () => {
                    let container = document.getElementById('divSearchFlight');
                    if (container) {
                        let input = container.querySelector('input.srchBtnSe');
                        if (input) {
                            input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            
                            // Dispatch click event
                            let event = new MouseEvent('click', {
                                view: window,
                                bubbles: true,
                                cancelable: true
                            });
                            input.dispatchEvent(event);
                            
                            console.log('Search input clicked');
                        }
                    }
                }
                """)
                print("✓ Search input clicked via JavaScript")
            except Exception as e2:
                print(f"⚠ JavaScript click also failed: {e2}")
        
        # Wait for page navigation
        page.wait_for_timeout(1000)
        
        print(f"📍 Current URL: {page.url}")
        
        # Check if page navigated
        try:
            page.wait_for_url("**/Flight**", timeout=5000)
            print("✓ Page navigated to flight results!")
        except:
            print("⚠ Page did not navigate to results within 5 seconds")
        
        page.wait_for_timeout(600)
        
        # First, remove any overlays that might be blocking
        page.evaluate("""
        () => {
            let overlays = document.querySelectorAll('[id*="overlay"], [class*="overlay"], [class*="modal"], [class*="backdrop"]');
            overlays.forEach(el => {
                if (el && el.style) {
                    el.style.display = 'none';
                }
            });
        }
        """)
        print("✓ Overlays cleared")
        page.wait_for_timeout(1000)
        
        # Find all buttons and their classes
        all_btn_classes = page.evaluate("""
        () => {
            let allButtons = document.querySelectorAll('button');
            let buttons = [];
            allButtons.forEach((btn, index) => {
                buttons.push({
                    index: index,
                    className: btn.className,
                    id: btn.id,
                    value: btn.value || '',
                    text: btn.textContent.substring(0, 30)
                });
            });
            return buttons;
        }
        """)
        print(f"\n📋 All buttons found:")
        for btn in all_btn_classes[:10]:  # Show first 10
            print(f"  {btn}")
        
        # Find search button by value
        btn_info = page.evaluate("""
        () => {
            let allButtons = document.querySelectorAll('button');
            let searchBtn = null;
            
            // Look for button with Search text or srchBtnSe class
            for (let btn of allButtons) {
                if (btn.value === 'Search' || btn.textContent.includes('Search') || btn.classList.contains('srchBtnSe')) {
                    searchBtn = btn;
                    break;
                }
            }
            
            if (searchBtn) {
                return {
                    found: true,
                    className: searchBtn.className,
                    id: searchBtn.id,
                    value: searchBtn.value,
                    text: searchBtn.textContent
                };
            }
            return { found: false };
        }
        """)
        print(f"\n🔘 Search Button Info: {btn_info}")
        
        try:
            # Scroll and click the Search button (srchBtnSe with value="Search")
            page.evaluate("""
            () => {
                let btn = document.querySelector('button.srchBtnSe[value="Search"]');
                if (!btn) btn = document.querySelector('button.srchBtnSe');
                if (btn) {
                    btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    if (btn.disabled) btn.disabled = false;
                    btn.style.pointerEvents = 'auto';
                    btn.style.opacity = '1';
                    btn.style.visibility = 'visible';
                }
            }
            """)
            print("✓ Search button visibility ensured via JavaScript")
            page.wait_for_timeout(600)
            
            # Try clicking with the correct locator
            page.locator("button.srchBtnSe").first.click(timeout=5000, force=True)
            print("✓ Search button CLICKED (First Click)!")
            clicked = True
        except Exception as e:
            print(f"⚠ Direct click failed: {str(e)[:100]}")
            
            # Method 2: JavaScript click
            try:
                page.evaluate("""
                () => {
                    let btn = document.querySelector('button.srchBtnSe[value="Search"]');
                    if (!btn) btn = document.querySelector('button.srchBtnSe');
                    if (btn) {
                        btn.click();
                        console.log('Search button clicked via JavaScript');
                    }
                }
                """)
                print("✓ Search button clicked via JavaScript! (First Click)")
                clicked = True
            except Exception as e2:
                print(f"⚠ JavaScript click also failed: {str(e2)[:100]}")
        
        # Second click attempt with additional events
        print("\n🔄 Attempting Second Click with Full Event Triggers...")
        try:
            page.evaluate("""
            () => {
                let btn = document.querySelector('button.srchBtnSe[value="Search"]');
                if (!btn) btn = document.querySelector('button.srchBtnSe');
                if (btn) {
                    // Trigger all necessary events
                    btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                    btn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                    btn.dispatchEvent(new MouseEvent('click', { bubbles: true }));
                    btn.click();
                    console.log('Search button clicked with all events - Second Click');
                }
            }
            """)
            print("✓ Search button clicked with full events! (Second Click)")
        except Exception as e:
            print(f"⚠ Second click failed: {str(e)[:100]}")
        
        page.wait_for_timeout(1000)
        
        print("\n🔍 Checking Button Handler and Form Fields...")
        
        # Check button's onclick handler
        btn_handler = page.evaluate("""
        () => {
            let btn = document.querySelector('button.srchBtnSe[value="Search"]');
            if (!btn) btn = document.querySelector('button.srchBtnSe');
            if (btn) {
                return {
                    onclick: btn.onclick ? 'Has onclick handler' : 'No onclick',
                    getAttribute: btn.getAttribute('onclick'),
                    eventListeners: 'Check browser DevTools'
                };
            }
            return { error: 'Button not found' };
        }
        """)
        print(f"Button handler info: {btn_handler}")
        
        # Check form fields for validation
        form_fields = page.evaluate("""
        () => {
            let fields = {};
            
            // Check all inputs
            let inputs = document.querySelectorAll('input[type="text"], input[type="hidden"], input[type="date"]');
            inputs.forEach(input => {
                if (input.name || input.id) {
                    fields[input.name || input.id] = {
                        value: input.value,
                        required: input.required,
                        valid: input.validity ? input.validity.valid : 'N/A'
                    };
                }
            });
            
            return fields;
        }
        """)
        print(f"Form fields check: {str(form_fields)[:300]}")
        
        # Try triggering any form submit event
        print("\n🚀 Attempting AJAX/Async Submit...")
        page.evaluate("""
        () => {
            let btn = document.querySelector('button.btn-refer.btn-block');
            if (btn && btn.onclick) {
                btn.onclick.call(btn);
            }
        }
        """)
        
        page.wait_for_timeout(1000)
        
        final_url = page.url
        
        # Debug: Check if there are any error messages or validation errors
        error_msg = page.evaluate("""
        () => {
            let errors = [];
            
            // Look for error messages
            let errorElements = document.querySelectorAll('[class*="error"], [class*="alert"], [class*="danger"], .err');
            errorElements.forEach(el => {
                if (el.textContent && el.textContent.trim()) {
                    errors.push(el.textContent.trim().substring(0, 100));
                }
            });
            
            // Check for required field errors
            let requiredFields = document.querySelectorAll('input[required], select[required]');
            requiredFields.forEach(field => {
                if (!field.value && field.offsetParent !== null) {
                    errors.push(`Required field empty: ${field.name || field.id}`);
                }
            });
            
            return {
                errors: errors,
                currentURL: window.location.href,
                pageTitle: document.title
            };
        }
        """)
        
        print("\n✅ Flight Search Results Page Loaded!")
        print(f"📍 Results URL: {page.url}\n")
        
        # Step 7: Click Book Now button
        print("🔍 STEP 3: Clicking Book Now button (id='BtnBookNow')...\n")
        
        page.wait_for_timeout(1000)
        
        try:
            # Find Book Now button info
            btn_info = page.evaluate("""
            () => {
                let btn = document.getElementById('BtnBookNow');
                if (btn) {
                    return {
                        found: true,
                        tagName: btn.tagName,
                        className: btn.className,
                        text: btn.textContent.trim().substring(0, 50),
                        visible: btn.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            print(f"📌 Book Now Button Info: {btn_info}\n")
            
            if btn_info.get('found'):
                # Try Playwright click first
                try:
                    page.locator("#BtnBookNow").click(timeout=5000, force=True)
                    print("✓ Book Now button clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback to JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let btn = document.getElementById('BtnBookNow');
                            if (btn) {
                                btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                
                                let event = new MouseEvent('click', {
                                    view: window,
                                    bubbles: true,
                                    cancelable: true
                                });
                                btn.dispatchEvent(event);
                                
                                if (btn.onclick) {
                                    btn.onclick.call(btn, event);
                                }
                                
                                console.log('Book Now button clicked via JavaScript');
                            }
                        }
                        """)
                        print("✓ Book Now button clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
            else:
                print("⚠ Book Now button not found on this page")
        except Exception as e:
            print(f"✗ Error clicking Book Now: {e}")
        
        # Wait for page navigation
        page.wait_for_timeout(1000)
        
        print(f"\n📍 Current URL: {page.url}")
        
        # Check if page navigated to booking page
        print("Waiting for page navigation...")
        
        page.wait_for_timeout(600)
        
        # Step 8: Check for "More Fare Options Available" and click "Book Now" under More Fares
        print("🔍 STEP 4: Checking for More Fare Options (Hidden Modal)...\n")
        
        # Check for the hidden More Fare Options modal
        try:
            more_fares_modal_info = page.evaluate("""
            () => {
                let modal = document.getElementById('DivMoreFareRT');
                let mfbookbtn = document.querySelector('._mfbookbtn');
                
                if (modal && mfbookbtn) {
                    return {
                        found: true,
                        modal_display: window.getComputedStyle(modal).display,
                        button_visible: mfbookbtn.offsetParent !== null,
                        button_text: mfbookbtn.textContent.trim()
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 More Fares Modal Status: " + str(more_fares_modal_info) + "\n")
            
            if more_fares_modal_info.get('found'):
                print("✓ More Fares Modal and Book Now button detected\n")
                
                # Make the hidden modal and its contents visible
                print("🔓 Making More Fares modal visible...\n")
                try:
                    page.evaluate("""
                    () => {
                        // Show the hidden modal
                        let modal = document.getElementById('DivMoreFareRT');
                        if (modal) {
                            // Walk up and show all parent containers
                            let current = modal;
                            let depth = 0;
                            while (current && depth < 10) {
                                if (current.offsetParent === null) {
                                    current.style.display = 'block';
                                    current.style.visibility = 'visible';
                                    current.style.opacity = '1';
                                    current.style.pointerEvents = 'auto';
                                }
                                current = current.parentElement;
                                depth++;
                            }
                            console.log('More Fares modal made visible');
                        }
                    }
                    """)
                    print("✓ More Fares modal is now visible\n")
                except Exception as e:
                    print(f"⚠ Failed to show modal: {e}\n")
                
                page.wait_for_timeout(1000)
                
                # Now click the Book Now button under More Fares
                print("🖱️ Clicking Book Now button under More Fares...\n")
                try:
                    # Try Playwright click first
                    page.locator("._mfbookbtn").first.click(timeout=5000, force=True)
                    print("✓ Book Now button under More Fares clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback to JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let btn = document.querySelector('._mfbookbtn');
                            if (btn) {
                                btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                
                                let event = new MouseEvent('click', {
                                    view: window,
                                    bubbles: true,
                                    cancelable: true
                                });
                                btn.dispatchEvent(event);
                                
                                if (btn.onclick) {
                                    btn.onclick.call(btn, event);
                                }
                                
                                console.log('Book Now button under More Fares clicked via JavaScript');
                            }
                        }
                        """)
                        print("✓ Book Now button under More Fares clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(1000)
            else:
                print("ℹ More Fares modal not found - page may have navigated directly to booking\n")
        
        except Exception as e:
            print(f"⚠ Error checking for More Fares: {e}\n")
        
        page.wait_for_timeout(600)
        
        print("\n✅ Flight Search & Booking Automation Completed!")
        print(f"📍 Final URL: {page.url}\n")
        
        # Additional Step: Click on Book Now button to reveal passenger details form
        print("🔍 STEP 4.5: Clicking Book Now button to load passenger form...\n")
        
        try:
            # First, let's check all available buttons and find ones with "Book" text
            books_buttons_info = page.evaluate("""
            () => {
                let buttons = [];
                let allButtons = document.querySelectorAll('button, div[role="button"], [class*="btn"]');
                
                allButtons.forEach((btn, idx) => {
                    let text = btn.textContent ? btn.textContent.trim() : '';
                    if (text.toLowerCase().includes('book')) {
                        buttons.push({
                            index: idx,
                            tag: btn.tagName,
                            id: btn.id,
                            className: btn.className,
                            text: text.substring(0, 50),
                            visible: btn.offsetParent !== null
                        });
                    }
                });
                
                return buttons;
            }
            """)
            
            if books_buttons_info:
                print(f"📌 Found {len(books_buttons_info)} button(s) with 'Book' text:")
                for btn_info in books_buttons_info:
                    print(f"   - {btn_info['tag']} (ID: {btn_info['id']}, Visible: {btn_info['visible']}): {btn_info['text']}")
                
                # Try to click the first visible "Book Now" button
                clicked = False
                for btn_info in books_buttons_info:
                    if btn_info['visible']:
                        try:
                            # Use ID if available, otherwise use text selector
                            if btn_info['id']:
                                page.locator(f"#{btn_info['id']}").click(timeout=5000, force=True)
                                print(f"✓ Clicked button with ID: {btn_info['id']}")
                            else:
                                # Use XPath to find by text
                                page.locator(f"//{btn_info['tag'].lower()}[contains(text(), 'Book')]").first.click(timeout=5000, force=True)
                                print(f"✓ Clicked {btn_info['tag']} button with 'Book' text")
                            
                            page.wait_for_timeout(1000)
                            clicked = True
                            break
                        except Exception as e:
                            print(f"⚠ Failed to click {btn_info['id'] or btn_info['text']}: {str(e)[:80]}")
                            continue
                
                if not clicked:
                    print("⚠ Could not click any visible 'Book' button")
            else:
                print("⚠ No buttons with 'Book' text found on page")
                
                # Last resort: try JavaScript to find and click
                print("\n🔍 Attempting JavaScript approach to find 'Book Now' button...")
                page.evaluate("""
                () => {
                    let buttons = document.querySelectorAll('button, div[role="button"]');
                    for (let btn of buttons) {
                        if (btn.textContent.toLowerCase().includes('book') && btn.offsetParent !== null) {
                            console.log('Found Book button via JS:', btn.textContent);
                            btn.click();
                            break;
                        }
                    }
                }
                """)
                print("✓ Attempted JavaScript click on Book button")
                page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"⚠ Error in Book Now button logic: {e}")
        
        page.wait_for_timeout(600)
        
        # Step 9: Click on Title dropdown for Adult
        print("🔍 STEP 5: Selecting Title for Adult...\n")
        
        try:
            # Wait for the title dropdown to appear
            page.wait_for_selector("#titleAdult0", timeout=10000)
            print("✓ Title dropdown for Adult found\n")
            
            # Get dropdown info
            title_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('titleAdult0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        type: dropdown.type,
                        name: dropdown.name,
                        id: dropdown.id,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Title Dropdown Info: " + str(title_dropdown_info) + "\n")
            
            if title_dropdown_info.get('found'):
                # Click on the title dropdown
                try:
                    page.locator("#titleAdult0").click(timeout=5000, force=True)
                    print("✓ Title dropdown for Adult clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback to JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('titleAdult0');
                            if (dropdown) {
                                dropdown.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                dropdown.click();
                                console.log('Title dropdown clicked via JavaScript');
                            }
                        }
                        """)
                        print("✓ Title dropdown for Adult clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(600)
                print(f"✓ Title dropdown is now open\n")
                
                # Select "Mr" from the dropdown
                print("🔍 Selecting 'Mr' from Title dropdown...\n")
                try:
                    page.locator("#titleAdult0").select_option("Mr")
                    print("✓ 'Mr' selected from Title dropdown via select_option\n")
                except Exception as e:
                    print(f"⚠ select_option failed: {e}")
                    
                    # Fallback: Find and click the Mr option
                    try:
                        page.locator("#titleAdult0 option", has_text="Mr").click(timeout=5000)
                        print("✓ 'Mr' option clicked via locator\n")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Try JavaScript approach
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('titleAdult0');
                                if (dropdown) {
                                    let options = dropdown.querySelectorAll('option');
                                    for (let opt of options) {
                                        if (opt.textContent.trim() === 'Mr') {
                                            opt.selected = true;
                                            dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                            console.log('Mr option selected via JavaScript');
                                            break;
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ 'Mr' selected via JavaScript\n")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection failed: {e3}\n")
                
                page.wait_for_timeout(1000)
        
        except Exception as e:
            print(f"⚠ Error with Title dropdown: {e}\n")
        
        # Step 10: Enter First Name for Adult
        print("🔍 STEP 6: Entering First Name for Adult...\n")
        
        try:
            # Wait for the First Name field to appear
            page.wait_for_selector("#txtFNAdult0", timeout=10000)
            print("✓ First Name field for Adult found\n")
            
            # Get field info
            first_name_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtFNAdult0');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 First Name Field Info: " + str(first_name_info) + "\n")
            
            if first_name_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtFNAdult0").click(timeout=5000, force=True)
                    print("✓ First Name field clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "Manni"
                try:
                    page.locator("#txtFNAdult0").fill("Manni")
                    print("✓ First Name 'Manni' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtFNAdult0").clear()
                        page.locator("#txtFNAdult0").type("Manni", delay=50)
                        print("✓ First Name 'Manni' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtFNAdult0');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ First Name field value: '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with First Name field: {e}\n")
        
        # Step 11: Enter Last Name for Adult
        print("🔍 STEP 7: Entering Last Name for Adult...\n")
        
        try:
            # Wait for the Last Name field to appear
            page.wait_for_selector("#txtLNAdult0", timeout=10000)
            print("✓ Last Name field for Adult found\n")
            
            # Get field info
            last_name_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtLNAdult0');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Last Name Field Info: " + str(last_name_info) + "\n")
            
            if last_name_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtLNAdult0").click(timeout=5000, force=True)
                    print("✓ Last Name field clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "Test"
                try:
                    page.locator("#txtLNAdult0").fill("Test")
                    print("✓ Last Name 'Test' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtLNAdult0").clear()
                        page.locator("#txtLNAdult0").type("Test", delay=50)
                        print("✓ Last Name 'Test' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtLNAdult0');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ Last Name field value: '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Last Name field: {e}\n")
        
        # Step 12: Click on Title dropdown for Child
        print("🔍 STEP 8: Selecting Title for Child...\n")
        
        try:
            # Wait for the title dropdown to appear
            page.wait_for_selector("#titleChild0", timeout=10000)
            print("✓ Title dropdown for Child found\n")
            
            # Get dropdown info
            title_child_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('titleChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        type: dropdown.type,
                        name: dropdown.name,
                        id: dropdown.id,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Title Dropdown Info (Child): " + str(title_child_dropdown_info) + "\n")
            
            if title_child_dropdown_info.get('found'):
                # Click on the title dropdown
                try:
                    page.locator("#titleChild0").click(timeout=5000, force=True)
                    print("✓ Title dropdown for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback to JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('titleChild0');
                            if (dropdown) {
                                dropdown.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                dropdown.click();
                                console.log('Title dropdown clicked via JavaScript');
                            }
                        }
                        """)
                        print("✓ Title dropdown for Child clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Select "Miss" from the dropdown
                print("🔍 Selecting 'Miss' from Title dropdown (Child)...\n")
                try:
                    page.locator("#titleChild0").select_option("Miss")
                    print("✓ 'Miss' selected from Title dropdown via select_option\n")
                except Exception as e:
                    print(f"⚠ select_option failed: {e}")
                    
                    # Fallback: Find and click the Miss option
                    try:
                        page.locator("#titleChild0 option", has_text="Miss").click(timeout=5000)
                        print("✓ 'Miss' option clicked via locator\n")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Try JavaScript approach
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('titleChild0');
                                if (dropdown) {
                                    let options = dropdown.querySelectorAll('option');
                                    for (let opt of options) {
                                        if (opt.textContent.trim() === 'Miss') {
                                            opt.selected = true;
                                            dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                            console.log('Miss option selected via JavaScript');
                                            break;
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ 'Miss' selected via JavaScript\n")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection failed: {e3}\n")
                
                page.wait_for_timeout(1000)
        
        except Exception as e:
            print(f"⚠ Error with Title dropdown (Child): {e}\n")
        
        # Step 13: Enter First Name for Child
        print("🔍 STEP 9: Entering First Name for Child...\n")
        
        try:
            # Wait for the First Name field to appear
            page.wait_for_selector("#txtFNChild0", timeout=10000)
            print("✓ First Name field for Child found\n")
            
            # Get field info
            first_name_child_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtFNChild0');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 First Name Field Info (Child): " + str(first_name_child_info) + "\n")
            
            if first_name_child_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtFNChild0").click(timeout=5000, force=True)
                    print("✓ First Name field for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "Child"
                try:
                    page.locator("#txtFNChild0").fill("Child")
                    print("✓ First Name 'Child' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtFNChild0").clear()
                        page.locator("#txtFNChild0").type("Child", delay=50)
                        print("✓ First Name 'Child' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtFNChild0');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ First Name field value (Child): '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with First Name field (Child): {e}\n")
        
        # Step 14: Enter Last Name for Child
        print("🔍 STEP 10: Entering Last Name for Child...\n")
        
        try:
            # Wait for the Last Name field to appear
            page.wait_for_selector("#txtLNChild0", timeout=10000)
            print("✓ Last Name field for Child found\n")
            
            # Get field info
            last_name_child_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtLNChild0');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Last Name Field Info (Child): " + str(last_name_child_info) + "\n")
            
            if last_name_child_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtLNChild0").click(timeout=5000, force=True)
                    print("✓ Last Name field for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "Test"
                try:
                    page.locator("#txtLNChild0").fill("Test")
                    print("✓ Last Name 'Test' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtLNChild0").clear()
                        page.locator("#txtLNChild0").type("Test", delay=50)
                        print("✓ Last Name 'Test' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtLNChild0');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ Last Name field value (Child): '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Last Name field (Child): {e}\n")
        
        # Step 15: Click on Title dropdown for Infant
        print("🔍 STEP 11: Selecting Title for Infant...\n")
        
        try:
            # Wait for the title dropdown to appear
            page.wait_for_selector("#titleInfant0", timeout=10000)
            print("✓ Title dropdown for Infant found\n")
            
            # Get dropdown info
            title_infant_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('titleInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        type: dropdown.type,
                        name: dropdown.name,
                        id: dropdown.id,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Title Dropdown Info (Infant): " + str(title_infant_dropdown_info) + "\n")
            
            if title_infant_dropdown_info.get('found'):
                # Click on the title dropdown
                try:
                    page.locator("#titleInfant0").click(timeout=5000, force=True)
                    print("✓ Title dropdown for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback to JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('titleInfant0');
                            if (dropdown) {
                                dropdown.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                dropdown.click();
                                console.log('Title dropdown clicked via JavaScript');
                            }
                        }
                        """)
                        print("✓ Title dropdown for Infant clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Select "Master" from the dropdown
                print("🔍 Selecting 'Master' from Title dropdown (Infant)...\n")
                try:
                    page.locator("#titleInfant0").select_option("Master")
                    print("✓ 'Master' selected from Title dropdown via select_option\n")
                except Exception as e:
                    print(f"⚠ select_option failed: {e}")
                    
                    # Fallback: Find and click the Master option
                    try:
                        page.locator("#titleInfant0 option", has_text="Master").click(timeout=5000)
                        print("✓ 'Master' option clicked via locator\n")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Try JavaScript approach
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('titleInfant0');
                                if (dropdown) {
                                    let options = dropdown.querySelectorAll('option');
                                    for (let opt of options) {
                                        if (opt.textContent.trim() === 'Master') {
                                            opt.selected = true;
                                            dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                            console.log('Master option selected via JavaScript');
                                            break;
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ 'Master' selected via JavaScript\n")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection failed: {e3}\n")
                
                page.wait_for_timeout(1000)
        
        except Exception as e:
            print(f"⚠ Error with Title dropdown (Infant): {e}\n")
        
        # Step 16: Enter First Name for Infant
        print("🔍 STEP 12: Entering First Name for Infant...\n")
        
        try:
            # Wait for the First Name field to appear
            page.wait_for_selector("#txtFNInfant0", timeout=10000)
            print("✓ First Name field for Infant found\n")
            
            # Get field info
            first_name_infant_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtFNInfant0');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 First Name Field Info (Infant): " + str(first_name_infant_info) + "\n")
            
            if first_name_infant_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtFNInfant0").click(timeout=5000, force=True)
                    print("✓ First Name field for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "Infant"
                try:
                    page.locator("#txtFNInfant0").fill("Infant")
                    print("✓ First Name 'Infant' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtFNInfant0").clear()
                        page.locator("#txtFNInfant0").type("Infant", delay=50)
                        print("✓ First Name 'Infant' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtFNInfant0');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ First Name field value (Infant): '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with First Name field (Infant): {e}\n")
        
        # Step 17: Enter Last Name for Infant
        print("🔍 STEP 13: Entering Last Name for Infant...\n")
        
        try:
            # Wait for the Last Name field to appear
            page.wait_for_selector("#txtLNInfant0", timeout=10000)
            print("✓ Last Name field for Infant found\n")
            
            # Get field info
            last_name_infant_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtLNInfant0');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Last Name Field Info (Infant): " + str(last_name_infant_info) + "\n")
            
            if last_name_infant_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtLNInfant0").click(timeout=5000, force=True)
                    print("✓ Last Name field for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "Test"
                try:
                    page.locator("#txtLNInfant0").fill("Test")
                    print("✓ Last Name 'Test' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtLNInfant0").clear()
                        page.locator("#txtLNInfant0").type("Test", delay=50)
                        print("✓ Last Name 'Test' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtLNInfant0');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ Last Name field value (Infant): '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Last Name field (Infant): {e}\n")
        
        # Step 18: Select Day for Infant DOB
        print("🔍 STEP 14: Selecting Day for Infant DOB...\n")
        
        try:
            # Wait for the day dropdown to appear
            page.wait_for_selector("#divDOBDayInfant0", timeout=10000)
            print("✓ Day dropdown for Infant DOB found\n")
            
            # Get dropdown info
            day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBDayInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        name: dropdown.name,
                        id: dropdown.id,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Day Dropdown Info (Infant DOB): " + str(day_dropdown_info) + "\n")
            
            if day_dropdown_info.get('found'):
                # Select "10" from the dropdown
                print("🔍 Selecting '10' from Day dropdown (Infant DOB)...\n")
                try:
                    page.locator("#divDOBDayInfant0").select_option("10")
                    print("✓ Day '10' selected from dropdown via select_option\n")
                except Exception as e:
                    print(f"⚠ select_option failed: {e}")
                    
                    # Fallback: Use JavaScript
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBDayInfant0');
                            if (dropdown) {
                                dropdown.value = '10';
                                dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                console.log('Day 10 selected via JavaScript');
                            }
                        }
                        """)
                        print("✓ Day '10' selected via JavaScript\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript selection failed: {e2}\n")
                
                page.wait_for_timeout(500)
        
        except Exception as e:
            print(f"⚠ Error with Day dropdown (Infant DOB): {e}\n")
        
        # Step 19: Select Month for Infant DOB
        print("🔍 STEP 15: Selecting Month for Infant DOB...\n")
        
        try:
            # Wait for the month dropdown to appear
            page.wait_for_selector("#divDOBMonInfant0", timeout=10000)
            print("✓ Month dropdown for Infant DOB found\n")
            
            # Get dropdown info
            month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBMonInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        name: dropdown.name,
                        id: dropdown.id,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Month Dropdown Info (Infant DOB): " + str(month_dropdown_info) + "\n")
            
            if month_dropdown_info.get('found'):
                # Select "Jan" from the dropdown
                print("🔍 Selecting 'Jan' from Month dropdown (Infant DOB)...\n")
                try:
                    page.locator("#divDOBMonInfant0").select_option("Jan")
                    print("✓ Month 'Jan' selected from dropdown via select_option\n")
                except Exception as e:
                    print(f"⚠ select_option failed: {e}")
                    
                    # Fallback: Use JavaScript
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBMonInfant0');
                            if (dropdown) {
                                dropdown.value = 'Jan';
                                dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                console.log('Month Jan selected via JavaScript');
                            }
                        }
                        """)
                        print("✓ Month 'Jan' selected via JavaScript\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript selection failed: {e2}\n")
                
                page.wait_for_timeout(500)
        
        except Exception as e:
            print(f"⚠ Error with Month dropdown (Infant DOB): {e}\n")
        
        # Step 20: Select Year for Infant DOB
        print("🔍 STEP 16: Selecting Year for Infant DOB...\n")
        
        try:
            # Wait for the year dropdown to appear
            page.wait_for_selector("#divDOBYarInfant0", timeout=10000)
            print("✓ Year dropdown for Infant DOB found\n")
            
            # Get dropdown info
            year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBYarInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        name: dropdown.name,
                        id: dropdown.id,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Year Dropdown Info (Infant DOB): " + str(year_dropdown_info) + "\n")
            
            if year_dropdown_info.get('found'):
                # Select "2026" from the dropdown
                print("🔍 Selecting '2026' from Year dropdown (Infant DOB)...\n")
                try:
                    page.locator("#divDOBYarInfant0").select_option("2026")
                    print("✓ Year '2026' selected from dropdown via select_option\n")
                except Exception as e:
                    print(f"⚠ select_option failed: {e}")
                    
                    # Fallback: Use JavaScript
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBYarInfant0');
                            if (dropdown) {
                                dropdown.value = '2026';
                                dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                console.log('Year 2026 selected via JavaScript');
                            }
                        }
                        """)
                        print("✓ Year '2026' selected via JavaScript\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript selection failed: {e2}\n")
                
                page.wait_for_timeout(500)
        
        except Exception as e:
            print(f"⚠ Error with Year dropdown (Infant DOB): {e}\n")
        
        # Step 21: Enter Email Address under Contact Details
        print("🔍 STEP 17: Entering Email Address under Contact Details...\n")
        
        try:
            # Wait for the email field to appear
            page.wait_for_selector("#txtEmailId", timeout=10000)
            print("✓ Email Address field found\n")
            
            # Get field info
            email_field_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtEmailId');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Email Address Field Info: " + str(email_field_info) + "\n")
            
            if email_field_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtEmailId").click(timeout=5000, force=True)
                    print("✓ Email Address field clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter the email
                try:
                    page.locator("#txtEmailId").fill("manish.dasila@easemytrip.com")
                    print("✓ Email Address 'manish.dasila@easemytrip.com' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtEmailId").clear()
                        page.locator("#txtEmailId").type("manish.dasila@easemytrip.com", delay=25)
                        print("✓ Email Address 'manish.dasila@easemytrip.com' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtEmailId');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ Email Address field value: '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Email Address field: {e}\n")
        
        # Step 22: Enter Mobile Number under Contact Details
        print("🔍 STEP 18: Entering Mobile Number under Contact Details...\n")
        
        try:
            # Wait for the mobile field to appear
            page.wait_for_selector("#txtCPhone", timeout=10000)
            print("✓ Mobile Number field found\n")
            
            # Get field info
            mobile_field_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtCPhone');
                if (field) {
                    return {
                        found: true,
                        tagName: field.tagName,
                        type: field.type,
                        name: field.name,
                        id: field.id,
                        value: field.value,
                        visible: field.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Mobile Number Field Info: " + str(mobile_field_info) + "\n")
            
            if mobile_field_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtCPhone").click(timeout=5000, force=True)
                    print("✓ Mobile Number field clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter the mobile number
                try:
                    page.locator("#txtCPhone").fill("9999999999")
                    print("✓ Mobile Number '9999999999' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtCPhone").clear()
                        page.locator("#txtCPhone").type("9999999999", delay=25)
                        print("✓ Mobile Number '9999999999' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtCPhone');
                    if (field) {
                        return {
                            value: field.value,
                            length: field.value.length
                        };
                    }
                    return null;
                }
                """)
                
                if entered_value:
                    print(f"✓ Mobile Number field value: '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Mobile Number field: {e}\n")
        
        # Step 23: Click on Insurance Radio Button
        print("🔍 STEP 19: Clicking on Insurance Radio Button...\n")
        
        try:
            # Wait for the insurance radio button to appear
            page.wait_for_selector("#chkInsurance", timeout=10000)
            print("✓ Insurance Radio Button found\n")
            
            # Get radio button info
            insurance_info = page.evaluate("""
            () => {
                let element = document.getElementById('chkInsurance');
                if (element) {
                    return {
                        found: true,
                        tagName: element.tagName,
                        type: element.type,
                        name: element.name,
                        id: element.id,
                        checked: element.checked,
                        visible: element.offsetParent !== null,
                        text: element.parentElement ? element.parentElement.textContent.trim() : ''
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Insurance Radio Button Info: " + str(insurance_info) + "\n")
            
            if insurance_info.get('found'):
                # Click on the radio button
                try:
                    page.locator("#chkInsurance").click(timeout=5000, force=True)
                    print("✓ Insurance Radio Button clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let element = document.getElementById('chkInsurance');
                            if (element) {
                                element.click();
                                element.checked = true;
                                element.dispatchEvent(new Event('change', { bubbles: true }));
                                return true;
                            }
                            return false;
                        }
                        """)
                        print("✓ Insurance Radio Button clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the radio button was selected
                verified_state = page.evaluate("""
                () => {
                    let element = document.getElementById('chkInsurance');
                    if (element) {
                        return {
                            checked: element.checked,
                            parentText: element.parentElement ? element.parentElement.textContent.trim() : ''
                        };
                    }
                    return null;
                }
                """)
                
                if verified_state:
                    print(f"✓ Insurance Radio Button Checked: {verified_state.get('checked')}")
                    print(f"✓ Associated Text: {verified_state.get('parentText')}\n")
                else:
                    print("⚠ Could not verify radio button state\n")
        
        except Exception as e:
            print(f"⚠ Error with Insurance Radio Button: {e}\n")
        
        # Step 24: Click Continue Booking Button
        print("🔍 STEP 20: Clicking Continue Booking Button...\n")
        
        try:
            # Wait for the continue booking button to appear
            page.wait_for_selector("#spnTransaction", timeout=10000)
            print("✓ Continue Booking button found\n")
            
            # Get button info
            continue_booking_info = page.evaluate("""
            () => {
                let element = document.getElementById('spnTransaction');
                if (element) {
                    return {
                        found: true,
                        tagName: element.tagName,
                        className: element.className,
                        id: element.id,
                        text: element.textContent.trim(),
                        visible: element.offsetParent !== null,
                        innerHTML: element.innerHTML.substring(0, 100)
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Continue Booking Button Info: " + str(continue_booking_info) + "\n")
            
            if continue_booking_info.get('found'):
                # Click on the button
                try:
                    page.locator("#spnTransaction").click(timeout=5000, force=True)
                    print("✓ Continue Booking button clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let element = document.getElementById('spnTransaction');
                            if (element) {
                                element.click();
                                element.dispatchEvent(new Event('click', { bubbles: true }));
                                return true;
                            }
                            return false;
                        }
                        """)
                        print("✓ Continue Booking button clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Get current URL after click
                current_url = page.url
                print(f"✓ Current URL after Continue Booking click: {current_url}\n")
        
        except Exception as e:
            print(f"⚠ Error with Continue Booking button: {e}\n")
        
        # Step 20.5: Handle Free Cancellation Popup
        print("🔍 STEP 20.5: Handling Free Cancellation Popup...\n")
        
        try:
            # Wait for popup to potentially appear and become visible
            popup_appeared = False
            attempts = 0
            max_attempts = 15
            
            # Try to detect and click the Secure My Trip button
            while attempts < max_attempts and not popup_appeared:
                attempts += 1
                page.wait_for_timeout(300)
                
                # Check for the button with multiple selectors
                btn_info = page.evaluate("""
                () => {
                    // Try multiple selectors for the button
                    let btn = document.querySelector('button.conf_btn') ||
                              document.querySelector('[class*="conf_btn"]') ||
                              document.querySelector('button.btn-primary') ||
                              Array.from(document.querySelectorAll('button')).find(b => 
                                  b.textContent.includes('Secure') || 
                                  b.textContent.includes('Trip') ||
                                  b.className.includes('conf')
                              ) ||
                              Array.from(document.querySelectorAll('div[role="button"]')).find(b => 
                                  b.textContent.includes('Secure') || 
                                  b.textContent.includes('Trip')
                              );
                    
                    if (btn) {
                        return {
                            found: true,
                            text: btn.textContent.trim().substring(0, 50),
                            className: btn.className,
                            tag: btn.tagName,
                            visible: btn.offsetParent !== null,
                            display: window.getComputedStyle(btn).display
                        };
                    }
                    return { found: false };
                }
                """)
                
                if btn_info.get('found'):
                    popup_appeared = True
                    print(f"📌 Free Cancellation Popup detected on attempt {attempts}")
                    print(f"📌 Button Info: {btn_info}\n")
                    
                    # Click the button
                    try:
                        # First try with button.conf_btn
                        try:
                            page.locator("button.conf_btn").click(timeout=3000, force=True)
                            print("✓ 'Secure My Trip' button clicked via button.conf_btn selector")
                        except:
                            # Try attribute selector
                            try:
                                page.locator('[class*="conf_btn"]').click(timeout=3000, force=True)
                                print("✓ 'Secure My Trip' button clicked via attribute selector")
                            except:
                                # Try by text content
                                try:
                                    page.locator("button:has-text('Secure')").click(timeout=3000, force=True)
                                    print("✓ 'Secure My Trip' button clicked via text selector")
                                except:
                                    raise Exception("All Playwright selectors failed")
                    except Exception as e:
                        print(f"⚠ Playwright click failed: {e}")
                        
                        # Fallback: Use JavaScript click
                        try:
                            page.evaluate("""
                            () => {
                                let btn = document.querySelector('button.conf_btn') ||
                                          document.querySelector('[class*="conf_btn"]') ||
                                          Array.from(document.querySelectorAll('button')).find(b => 
                                              b.textContent.includes('Secure') || 
                                              b.textContent.includes('Trip')
                                          );
                                
                                if (btn) {
                                    btn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                    
                                    // Dispatch multiple events to ensure click is registered
                                    let mousedownEvent = new MouseEvent('mousedown', {
                                        view: window,
                                        bubbles: true,
                                        cancelable: true
                                    });
                                    let clickEvent = new MouseEvent('click', {
                                        view: window,
                                        bubbles: true,
                                        cancelable: true
                                    });
                                    let mouseupEvent = new MouseEvent('mouseup', {
                                        view: window,
                                        bubbles: true,
                                        cancelable: true
                                    });
                                    
                                    btn.dispatchEvent(mousedownEvent);
                                    btn.dispatchEvent(clickEvent);
                                    btn.dispatchEvent(mouseupEvent);
                                    btn.click();
                                    
                                    console.log('Secure My Trip button clicked via JavaScript');
                                    return true;
                                }
                                return false;
                            }
                            """)
                            print("✓ 'Secure My Trip' button clicked via JavaScript")
                        except Exception as e2:
                            print(f"⚠ JavaScript click also failed: {e2}")
                    
                    page.wait_for_timeout(800)
                    print("✓ Free Cancellation popup handled\n")
                    break
            
            if not popup_appeared:
                print("ℹ Free Cancellation popup not detected (may not have appeared or already closed)\n")
        
        except Exception as e:
            print(f"⚠ Error handling Free Cancellation popup: {e}\n")
        
        # Step 25: Skip on Seat Selection Popup
        print("🔍 STEP 21: Skipping on Seat Selection Popup...\n")
        
        try:
            # Wait a moment for the popup to appear
            page.wait_for_timeout(600)
            
            # Try to find the Skip button - look for common patterns
            skip_button = None
            skip_selectors = [
                "text=Skip",
                "button:has-text('Skip')",
                "[class*='skip']",
                "[class*='Skip']",
                "a:has-text('Skip')",
                "span:has-text('Skip')"
            ]
            
            print("🔍 Looking for Skip button on seat selection popup...\n")
            
            for selector in skip_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        skip_button = page.locator(selector).first
                        print(f"✓ Skip button found with selector: {selector}")
                        break
                except:
                    continue
            
            if skip_button:
                try:
                    skip_button.click(timeout=5000, force=True)
                    print("✓ Skip button clicked via Playwright\n")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let skipBtn = Array.from(document.querySelectorAll('*')).find(el => 
                                el.textContent.includes('Skip') && 
                                (el.tagName === 'BUTTON' || el.tagName === 'A' || el.tagName === 'SPAN')
                            );
                            if (skipBtn) {
                                skipBtn.click();
                                return true;
                            }
                            return false;
                        }
                        """)
                        print("✓ Skip button clicked via JavaScript\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}\n")
                
                page.wait_for_timeout(600)
                
                # Get current URL after skip
                current_url = page.url
                print(f"✓ Current URL after Skip: {current_url}\n")
            else:
                print("⚠ Skip button not found on popup\n")
        
        except Exception as e:
            print(f"⚠ Error with Seat Selection Popup Skip: {e}\n")
        
        # Step 26: Skip to Payment Button
        print("🔍 STEP 22: Clicking Skip to Payment Button...\n")
        
        try:
            # Wait for the skip to payment button to appear
            page.wait_for_selector("#skipPop", timeout=10000)
            print("✓ Skip to Payment button found\n")
            
            # Get button info
            skip_payment_info = page.evaluate("""
            () => {
                let element = document.getElementById('skipPop');
                if (element) {
                    return {
                        found: true,
                        tagName: element.tagName,
                        className: element.className,
                        id: element.id,
                        text: element.textContent.trim(),
                        visible: element.offsetParent !== null,
                        innerHTML: element.innerHTML.substring(0, 100)
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Skip to Payment Button Info: " + str(skip_payment_info) + "\n")
            
            if skip_payment_info.get('found'):
                # Click on the button
                try:
                    page.locator("#skipPop").click(timeout=5000, force=True)
                    print("✓ Skip to Payment button clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let element = document.getElementById('skipPop');
                            if (element) {
                                element.click();
                                element.dispatchEvent(new Event('click', { bubbles: true }));
                                return true;
                            }
                            return false;
                        }
                        """)
                        print("✓ Skip to Payment button clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(2000)
                
                # Get current URL after skip
                current_url = page.url
                print(f"✓ Current URL after Skip to Payment: {current_url}\n")
        
        except Exception as e:
            print(f"⚠ Error with Skip to Payment button: {e}\n")
        
        # Step 27: Click on Payment Method Option (Mobikwik, Payzapp, PhonePe, Amazon)
        print("🔍 STEP 23: Clicking on Payment Method Option (Mobikwik, Payzapp, PhonePe, Amazon)...\n")
        
        try:
            # Wait a moment for payment page to load - CRITICAL: payment gateways need time to render
            page.wait_for_timeout(3000)
            
            # Get all elements with the class
            payment_method_info = page.evaluate("""
            () => {
                let elements = document.querySelectorAll('.pymtsbtxt');
                let results = [];
                elements.forEach((el, idx) => {
                    results.push({
                        index: idx,
                        text: el.textContent.trim().substring(0, 100),
                        className: el.className,
                        visible: el.offsetParent !== null,
                        tagName: el.tagName,
                        parent: el.parentElement ? el.parentElement.className : ''
                    });
                });
                return results;
            }
            """)
            
            print("📌 Payment Method Elements Found: " + str(len(payment_method_info)) + "\n")
            for i, info in enumerate(payment_method_info):
                print(f"  Element {i}: {info.get('text', 'N/A')}")
            
            # Find the index of the element containing "Choose Mobikwik"
            target_index = None
            for i, info in enumerate(payment_method_info):
                if "Choose Mobikwik" in info.get('text', ''):
                    target_index = i
                    print(f"\n✓ Found target element at index {target_index}\n")
                    break
            
            if target_index is not None:
                print(f"🔍 Attempting to click on element index {target_index}...\n")
                
                # Try multiple methods to click
                clicked = False
                
                # Method 1: Scroll to element first
                try:
                    page.evaluate(f"""
                    () => {{
                        let elements = document.querySelectorAll('.pymtsbtxt');
                        if (elements[{target_index}]) {{
                            elements[{target_index}].scrollIntoView({{behavior: 'smooth', block: 'center'}});
                        }}
                    }}
                    """)
                    print("✓ Scrolled to element")
                    page.wait_for_timeout(1000)
                except Exception as e:
                    print(f"⚠ Scroll failed: {e}")
                
                # Method 2: Playwright click on the nth element
                try:
                    all_elements = page.locator(".pymtsbtxt")
                    print(f"📌 Total elements found by Playwright: {all_elements.count()}")
                    
                    # Get the specific element
                    target_element = all_elements.nth(target_index)
                    target_element.click(timeout=5000, force=True)
                    print(f"✓ Payment Method clicked via Playwright (nth locator)\n")
                    clicked = True
                except Exception as e:
                    print(f"⚠ Playwright nth click failed: {e}\n")
                
                # Method 3: JavaScript click if Playwright click didn't work
                if not clicked:
                    try:
                        result = page.evaluate(f"""
                        () => {{
                            let elements = document.querySelectorAll('.pymtsbtxt');
                            let element = elements[{target_index}];
                            if (element) {{
                                console.log('Clicking element:', element.textContent);
                                // Ensure element is visible
                                element.style.visibility = 'visible';
                                element.style.display = 'block';
                                element.style.pointerEvents = 'auto';
                                
                                // Click the element
                                element.click();
                                
                                // Dispatch additional events
                                element.dispatchEvent(new Event('click', {{ bubbles: true, cancelable: true }}));
                                element.dispatchEvent(new Event('mousedown', {{ bubbles: true, cancelable: true }}));
                                element.dispatchEvent(new Event('mouseup', {{ bubbles: true, cancelable: true }}));
                                
                                return true;
                            }}
                            return false;
                        }}
                        """)
                        if result:
                            print(f"✓ Payment Method clicked via JavaScript\n")
                            clicked = True
                        else:
                            print(f"⚠ JavaScript click returned false\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click failed: {e2}\n")
                
                # Method 4: Try clicking parent element
                if not clicked:
                    try:
                        result = page.evaluate(f"""
                        () => {{
                            let elements = document.querySelectorAll('.pymtsbtxt');
                            let element = elements[{target_index}];
                            if (element && element.parentElement) {{
                                element.parentElement.click();
                                return true;
                            }}
                            return false;
                        }}
                        """)
                        if result:
                            print(f"✓ Parent element clicked via JavaScript\n")
                            clicked = True
                    except Exception as e3:
                        print(f"⚠ Parent click failed: {e3}\n")
                
                page.wait_for_timeout(600)
                
                # Get current URL after click
                current_url = page.url
                print(f"✓ Current URL after Payment Method click: {current_url}\n")
            else:
                print("⚠ Could not find element containing 'Choose Mobikwik'\n")
        
        except Exception as e:
            print(f"⚠ Error with Payment Method selection: {e}\n")
        
        # Step 28: Click on Bajaj Pay Radio Button
        print("🔍 STEP 24: Clicking on Bajaj Pay Radio Button...\n")
        
        try:
            # Wait a moment for the payment options to load - CRITICAL: more time for payment UI
            page.wait_for_timeout(2000)
            
            # Try to find the radio button
            try:
                page.wait_for_selector("#rdoBajaj Pay", timeout=10000)
                print("✓ Bajaj Pay radio button found\n")
            except:
                print("⚠ Radio button not found with exact ID, trying alternative selectors...\n")
            
            # Get radio button info
            bajaj_info = page.evaluate("""
            () => {
                // Try exact ID first
                let element = document.getElementById('rdoBajaj Pay');
                if (!element) {
                    // Try by name attribute
                    let elements = document.querySelectorAll('[name="walletP"]');
                    if (elements.length > 0) {
                        // Find the Bajaj Pay one
                        for (let el of elements) {
                            if (el.value && el.value.includes('Bajaj')) {
                                element = el;
                                break;
                            }
                        }
                    }
                }
                if (!element) {
                    // Try searching by text near radio button
                    let allRadios = document.querySelectorAll('input[type="radio"]');
                    for (let radio of allRadios) {
                        let label = radio.parentElement ? radio.parentElement.textContent : '';
                        if (label.includes('Bajaj Pay')) {
                            element = radio;
                            break;
                        }
                    }
                }
                if (element) {
                    return {
                        found: true,
                        id: element.id,
                        name: element.name,
                        type: element.type,
                        value: element.value,
                        checked: element.checked,
                        visible: element.offsetParent !== null,
                        labelText: element.parentElement ? element.parentElement.textContent.trim().substring(0, 100) : ''
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Bajaj Pay Radio Button Info: " + str(bajaj_info) + "\n")
            
            if bajaj_info.get('found'):
                # Get the ID to click
                button_id = bajaj_info.get('id')
                
                clicked = False
                
                # Method 1: Try clicking by ID if available
                if button_id:
                    try:
                        page.locator(f"#{button_id}").click(timeout=5000, force=True)
                        print(f"✓ Bajaj Pay radio button clicked via ID: {button_id}\n")
                        clicked = True
                    except Exception as e:
                        print(f"⚠ Click by ID failed: {e}")
                
                # Method 2: Try clicking by name and value
                if not clicked:
                    try:
                        # Find by name and click
                        page.evaluate("""
                        () => {
                            let elements = document.querySelectorAll('[name="walletP"]');
                            for (let el of elements) {
                                if (el.value && el.value.includes('Bajaj')) {
                                    el.click();
                                    el.checked = true;
                                    el.dispatchEvent(new Event('change', { bubbles: true }));
                                    return true;
                                }
                            }
                            return false;
                        }
                        """)
                        print("✓ Bajaj Pay radio button clicked via name selector\n")
                        clicked = True
                    except Exception as e:
                        print(f"⚠ Click by name failed: {e}")
                
                # Method 3: JavaScript click on found element
                if not clicked:
                    try:
                        page.evaluate("""
                        () => {
                            let allRadios = document.querySelectorAll('input[type="radio"]');
                            for (let radio of allRadios) {
                                let label = radio.parentElement ? radio.parentElement.textContent : '';
                                if (label.includes('Bajaj Pay')) {
                                    radio.click();
                                    radio.checked = true;
                                    radio.dispatchEvent(new Event('change', { bubbles: true }));
                                    radio.dispatchEvent(new Event('click', { bubbles: true }));
                                    return true;
                                }
                            }
                            return false;
                        }
                        """)
                        print("✓ Bajaj Pay radio button clicked via text search\n")
                        clicked = True
                    except Exception as e:
                        print(f"⚠ Click by text search failed: {e}")
                
                page.wait_for_timeout(1500)
                
                # Verify the radio button is now checked
                verify_state = page.evaluate("""
                () => {
                    let element = document.getElementById('rdoBajaj Pay');
                    if (!element) {
                        let elements = document.querySelectorAll('[name="walletP"]');
                        for (let el of elements) {
                            if (el.value && el.value.includes('Bajaj')) {
                                element = el;
                                break;
                            }
                        }
                    }
                    if (!element) {
                        let allRadios = document.querySelectorAll('input[type="radio"]');
                        for (let radio of allRadios) {
                            let label = radio.parentElement ? radio.parentElement.textContent : '';
                            if (label.includes('Bajaj Pay')) {
                                element = radio;
                                break;
                            }
                        }
                    }
                    if (element) {
                        return {
                            checked: element.checked,
                            value: element.value,
                            labelText: element.parentElement ? element.parentElement.textContent.trim().substring(0, 100) : ''
                        };
                    }
                    return null;
                }
                """)
                
                if verify_state:
                    print(f"✓ Bajaj Pay Radio Button Status: Checked = {verify_state.get('checked')}")
                    print(f"✓ Value: {verify_state.get('value')}")
                    print(f"✓ Label: {verify_state.get('labelText')}\n")
                else:
                    print("⚠ Could not verify radio button state\n")
            else:
                print("⚠ Bajaj Pay radio button not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Bajaj Pay radio button: {e}\n")
        
        page.wait_for_timeout(2000)
        
        # Step 25: Click Make Payment Button
        print("🔍 STEP 25: Clicking Make Payment Button...\n")
        
        try:
            # Get Make Payment button info
            make_payment_info = page.evaluate("""
            () => {
                let button = document.querySelector('.mk-pym4');
                if (!button) {
                    button = document.querySelector('[class*="mk-pym4"]');
                }
                if (!button) {
                    let buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.includes('Make Payment')) {
                            return {
                                found: true,
                                tagName: btn.tagName,
                                className: btn.className,
                                id: btn.id,
                                text: btn.textContent.trim().substring(0, 100),
                                visible: btn.offsetParent !== null,
                                type: btn.type
                            };
                        }
                    }
                }
                if (button) {
                    return {
                        found: true,
                        tagName: button.tagName,
                        className: button.className,
                        id: button.id,
                        text: button.textContent.trim().substring(0, 100),
                        visible: button.offsetParent !== null,
                        type: button.type
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Make Payment Button Info: " + str(make_payment_info) + "\n")
            
            if make_payment_info.get('found'):
                # Method 1: Try clicking via Playwright
                try:
                    page.locator(".mk-pym4").first.click(timeout=5000)
                    print("✓ Make Payment button clicked via Playwright\n")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Method 2: Try JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let button = document.querySelector('.mk-pym4');
                            if (!button) {
                                button = document.querySelector('[class*="mk-pym4"]');
                            }
                            if (!button) {
                                let buttons = document.querySelectorAll('button');
                                for (let btn of buttons) {
                                    if (btn.textContent.includes('Make Payment')) {
                                        button = btn;
                                        break;
                                    }
                                }
                            }
                            if (button) {
                                button.click();
                                button.dispatchEvent(new Event('click', { bubbles: true }));
                                button.dispatchEvent(new Event('mousedown', { bubbles: true }));
                                button.dispatchEvent(new Event('mouseup', { bubbles: true }));
                                return true;
                            }
                            return false;
                        }
                        """)
                        print("✓ Make Payment button clicked via JavaScript\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click failed: {e2}\n")
                
                page.wait_for_timeout(1000)
                
                # Check final URL after clicking
                final_url = page.url
                print(f"✓ Current URL after Make Payment click: {final_url}\n")
                
            else:
                print("⚠ Make Payment button not found on page\n")
        
        except Exception as e:
            print(f"⚠ Error with Make Payment button: {e}\n")
        
        page.wait_for_timeout(600)
        
        input("Press Enter to close the browser...")
        browser.close()

if __name__ == "__main__":
    search_flight()

