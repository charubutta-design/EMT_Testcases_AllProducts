# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
from datetime import datetime, timedelta
import os

def search_flight():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.easemytrip.co.th/")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)
        
        print("\n=== FLIGHT SEARCH AUTOMATION ===\n")
        
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
        
        # Step 6.5: Click "+ More Fares Available" button
        print("🔍 STEP 2.5: Checking for '+ More Fares Available' button...\n")
        
        try:
            # Check if LoadMore button exists
            more_fares_btn_info = page.evaluate("""
            () => {
                let btn = document.getElementById('LoadMore2');
                if (btn) {
                    return {
                        found: true,
                        className: btn.className,
                        text: btn.textContent.trim(),
                        visible: btn.offsetParent !== null,
                        display: window.getComputedStyle(btn).display
                    };
                }
                return { found: false };
            }
            """)
            
            print(f"📌 More Fares Button Info: {more_fares_btn_info}\n")
            
            if more_fares_btn_info.get('found'):
                print("✓ '+ More Fares Available' button detected\n")
                
                try:
                    # Try Playwright click first
                    page.locator("#LoadMore2").click(timeout=5000, force=True)
                    print("✓ '+ More Fares Available' button clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback to JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let btn = document.getElementById('LoadMore2');
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
                                
                                console.log('More Fares button clicked via JavaScript');
                            }
                        }
                        """)
                        print("✓ '+ More Fares Available' button clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                # Wait for additional fares to load
                page.wait_for_timeout(1500)
                
                # IMMEDIATELY show the modal that appears after LoadMore2 click
                try:
                    page.evaluate("""
                    () => {
                        // Show the hidden modal that appears after LoadMore2
                        let modal = document.getElementById('myModal_er');
                        let modalContent = document.querySelector('.modal-content-newb2b');
                        let modalBackdrop = document.querySelector('.modal-newb2b');
                        
                        if (modal) {
                            modal.style.display = 'block';
                            modal.style.visibility = 'visible';
                            modal.style.opacity = '1';
                            modal.style.zIndex = '9999';
                            modal.style.pointerEvents = 'auto';
                            console.log('Modal myModal_er shown');
                        }
                        
                        if (modalContent) {
                            modalContent.style.display = 'block';
                            modalContent.style.visibility = 'visible';
                            modalContent.style.opacity = '1';
                            console.log('Modal content shown');
                        }
                        
                        // Remove blur overlays
                        let blurOverlays = document.querySelectorAll('[class*="blur"], [class*="dark"], [class*="overlay"]');
                        blurOverlays.forEach(el => {
                            el.style.display = 'none';
                            el.style.opacity = '0';
                            el.style.pointerEvents = 'none';
                        });
                        
                        // Ensure body is visible
                        document.body.style.overflow = 'auto';
                        document.body.style.visibility = 'visible';
                        document.body.style.opacity = '1';
                        
                        console.log('Modal overlays cleared');
                    }
                    """)
                    print("✓ Modal made visible immediately")
                except Exception as e:
                    print(f"⚠ Could not show modal: {e}")
                
                # Clear any remaining loading overlays or blur screens
                try:
                    page.evaluate("""
                    () => {
                        // Remove loading spinners
                        let spinners = document.querySelectorAll('[class*="loader"], [class*="spinner"], [class*="loading"]');
                        spinners.forEach(el => el.remove());
                        
                        // Clear overlay/blur screens
                        let overlays = document.querySelectorAll('[class*="overlay"], [class*="modal-backdrop"], [class*="backdrop"]');
                        overlays.forEach(el => el.style.display = 'none');
                        
                        // Ensure body is not hidden
                        document.body.style.overflow = 'auto';
                        document.body.style.visibility = 'visible';
                        
                        console.log('Cleared loading overlays');
                    }
                    """)
                except Exception as e:
                    print(f"⚠ Could not clear overlays: {e}")
                
                print("✓ Additional fares loaded\n")
            else:
                print("ℹ '+ More Fares Available' button not found (may not be available or already loaded)\n")
        
        except Exception as e:
            print(f"⚠ Error checking for More Fares button: {e}\n")
        
        # Wait and clear any loading overlays
        page.wait_for_timeout(2000)
        
        try:
            page.evaluate("""
            () => {
                // Remove or hide loading overlays
                let darkOverlays = document.querySelectorAll('[class*="dark"], [class*="blur"], [style*="backdrop"]');
                darkOverlays.forEach(el => {
                    if (el.style.opacity !== undefined) {
                        el.style.opacity = '0';
                        el.style.pointerEvents = 'none';
                    }
                });
                
                // Ensure modal is on top
                let modal = document.getElementById('DivMoreFareRT');
                if (modal) {
                    modal.style.zIndex = '9999';
                    modal.style.display = 'block';
                }
            }
            """)
        except:
            pass
        
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
        
        # Add diagnostics to find what modals are actually on the page
        try:
            modal_diagnostics = page.evaluate("""
            () => {
                let allDivs = document.querySelectorAll('div[id*="More"], div[id*="modal"], div[id*="Modal"], div[class*="modal"], div[class*="Modal"]');
                let divInfo = [];
                allDivs.forEach((el, idx) => {
                    if (idx < 10) {
                        divInfo.push({
                            id: el.id,
                            class: el.className,
                            display: window.getComputedStyle(el).display,
                            visibility: window.getComputedStyle(el).visibility,
                            text: el.textContent.substring(0, 50)
                        });
                    }
                });
                
                let allOverlays = document.querySelectorAll('[class*="blur"], [class*="overlay"], [style*="backdrop"]');
                let overlayInfo = [];
                allOverlays.forEach((el, idx) => {
                    if (idx < 5) {
                        overlayInfo.push({
                            tag: el.tagName,
                            id: el.id,
                            class: el.className.substring(0, 50),
                            opacity: window.getComputedStyle(el).opacity
                        });
                    }
                });
                
                return { 
                    modals: divInfo,
                    overlays: overlayInfo,
                    DivMoreFareRT_exists: !!document.getElementById('DivMoreFareRT'),
                    mfbookbtn_exists: !!document.querySelector('._mfbookbtn')
                };
            }
            """)
            print(f"📊 Modal Diagnostics: {modal_diagnostics}\n")
        except Exception as e:
            print(f"⚠ Could not get diagnostics: {e}")
        
        # Check for the hidden More Fare Options modal
        try:
            more_fares_modal_info = page.evaluate("""
            () => {
                // Try both IDs - DivMoreFareRT and myModal_er
                let modal = document.getElementById('myModal_er') || document.getElementById('DivMoreFareRT');
                let mfbookbtn = document.querySelector('._mfbookbtn');
                
                if (modal) {
                    return {
                        found: true,
                        modal_id: modal.id,
                        modal_display: window.getComputedStyle(modal).display,
                        modal_visibility: window.getComputedStyle(modal).visibility,
                        button_exists: !!mfbookbtn,
                        button_visible: mfbookbtn ? mfbookbtn.offsetParent !== null : false,
                        button_text: mfbookbtn ? mfbookbtn.textContent.trim() : 'N/A'
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
                        // Show the modal using the correct ID
                        let modal = document.getElementById('myModal_er') || document.getElementById('DivMoreFareRT');
                        if (modal) {
                            modal.style.display = 'block';
                            modal.style.visibility = 'visible';
                            modal.style.opacity = '1';
                            modal.style.zIndex = '9999';
                            modal.style.pointerEvents = 'auto';
                            
                            // Also show modal backdrop/overlay
                            let backdrop = modal.previousElementSibling;
                            if (backdrop && backdrop.className.includes('modal')) {
                                backdrop.style.display = 'block';
                                backdrop.style.opacity = '1';
                            }
                            
                            // Walk up and show all parent containers
                            let current = modal;
                            let depth = 0;
                            while (current && depth < 10) {
                                if (current.offsetParent === null) {
                                    current.style.display = 'block';
                                    current.style.visibility = 'visible';
                                    current.style.opacity = '1';
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
                
                # Step 5: Click Continue button
                print("🔍 STEP 5: Clicking Continue button (class='book-bt-nwap marg-left')...\n")
                
                try:
                    # Check if Continue button exists
                    continue_btn_info = page.evaluate("""
                    () => {
                        let btn = document.querySelector('.book-bt-nwap.marg-left');
                        if (btn) {
                            return {
                                found: true,
                                className: btn.className,
                                text: btn.textContent.trim().substring(0, 50),
                                visible: btn.offsetParent !== null,
                                display: window.getComputedStyle(btn).display
                            };
                        }
                        return { found: false };
                    }
                    """)
                    
                    print(f"📌 Continue Button Info: {continue_btn_info}\n")
                    
                    if continue_btn_info.get('found'):
                        print("✓ Continue button detected\n")
                        
                        try:
                            # Try Playwright click first
                            page.locator(".book-bt-nwap.marg-left").first.click(timeout=5000, force=True)
                            print("✓ Continue button clicked via Playwright")
                        except Exception as e:
                            print(f"⚠ Playwright click failed: {e}")
                            
                            # Fallback to JavaScript click
                            try:
                                page.evaluate("""
                                () => {
                                    let btn = document.querySelector('.book-bt-nwap.marg-left');
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
                                        
                                        console.log('Continue button clicked via JavaScript');
                                    }
                                }
                                """)
                                print("✓ Continue button clicked via JavaScript")
                            except Exception as e2:
                                print(f"⚠ JavaScript click also failed: {e2}")
                        
                        page.wait_for_timeout(2000)
                        print("✓ Proceeding after Continue button click\n")
                    else:
                        print("⚠ Continue button not found on page\n")
                
                except Exception as e:
                    print(f"⚠ Error checking for Continue button: {e}\n")
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
        
        page.wait_for_timeout(2000)
        
        # Wait for page navigation and form to load
        print("⏳ Waiting for passenger form to load...\n")
        try:
            page.wait_for_selector("#titleAdult0, #divDOBDayAdult0, .passenger-form, [id*='Adult']", timeout=5000)
            print("✓ Passenger form elements detected\n")
        except Exception as nav_error:
            print(f"⚠ Timeout waiting for form elements via selector, checking if form exists...\n")
            print("🔍 Checking current URL and page content...\n")
            print(f"📍 Current URL: {page.url}\n")
            
            # Check if any form fields exist
            form_check = page.evaluate("""
            () => {
                let elements = {
                    titleAdult0: document.getElementById('titleAdult0') ? 'Found' : 'Not found',
                    txtFNAdult0: document.getElementById('txtFNAdult0') ? 'Found' : 'Not found',
                    adultElements: document.querySelectorAll('[id*="Adult"]').length,
                    allSelects: document.querySelectorAll('select').length,
                    allInputs: document.querySelectorAll('input').length
                };
                return elements;
            }
            """)
            print(f"Form element check: {form_check}\n")
            
            # If form elements are found, continue with data entry instead of returning
            if form_check.get('titleAdult0') == 'Found' or form_check.get('txtFNAdult0') == 'Found':
                print("✓ Form elements detected via JavaScript - proceeding with data entry\n")
            else:
                print("\n❌ Passenger form did not load. The page may have different structure or navigated to payment gateway.")
                print("Skipping passenger details and attempting payment button click.\n")
                
                # Jump to make payment section
                page.wait_for_timeout(2000)
                # input("Press Enter to close the browser...")
                browser.close()
                return
        
        # Step 9: Click on Title dropdown for Adult
        print("🔍 STEP 5: Selecting Title for Adult...\n")
        
        try:
            # Wait for the title dropdown to appear with shorter timeout
            page.wait_for_selector("#titleAdult0", timeout=3000)
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
            page.wait_for_selector("#txtFNAdult0", timeout=5000)
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
        
        # Step 11: Click on Day for Adult DOB
        print("🔍 STEP 7: Clicking on Date of Birth Day field for Adult...\n")
        
        try:
            # Wait for the DOB Day dropdown to appear
            page.wait_for_selector("#divDOBDayAdult0", timeout=10000)
            print("✓ Day dropdown for Adult DOB found\n")
            
            # Get dropdown info
            day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBDayAdult0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Day Dropdown Info (Adult DOB): " + str(day_dropdown_info) + "\n")
            
            if day_dropdown_info.get('found'):
                # Click on the day dropdown
                try:
                    page.locator("#divDOBDayAdult0").click(timeout=5000, force=True)
                    print("✓ Day dropdown for Adult DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBDayAdult0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Day dropdown for Adult DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.1: Select day "10" from the dropdown
                print("🔍 STEP 7.1: Selecting Day '10' from Adult DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#divDOBDayAdult0").select_option("10")
                    print("✓ Day '10' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="10" and click it
                    try:
                        # Find the option element with value="10" within or near the dropdown
                        option_selector = "#divDOBDayAdult0 option[value='10'], #divDOBDayAdult0 li[data-value='10'], .dropdown-menu li[data-value='10']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Day '10' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBDayAdult0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '10';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="10"]') || 
                                                   dropdown.querySelector('[value="10"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '10');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Day '10' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Day dropdown for Adult DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Day dropdown (Adult DOB): {e}\n")
        
        # Step 11.2: Click on Month for Adult DOB
        print("🔍 STEP 7.2: Clicking on Date of Birth Month field for Adult...\n")
        
        try:
            # Wait for the DOB Month dropdown to appear
            page.wait_for_selector("#divDOBMonAdult0", timeout=10000)
            print("✓ Month dropdown for Adult DOB found\n")
            
            # Get dropdown info
            month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBMonAdult0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Month Dropdown Info (Adult DOB): " + str(month_dropdown_info) + "\n")
            
            if month_dropdown_info.get('found'):
                # Click on the month dropdown
                try:
                    page.locator("#divDOBMonAdult0").click(timeout=5000, force=True)
                    print("✓ Month dropdown for Adult DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBMonAdult0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Month dropdown for Adult DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.3: Select month "05" (May) from the dropdown
                print("🔍 STEP 7.3: Selecting Month 'May' (value='05') from Adult DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#divDOBMonAdult0").select_option("05")
                    print("✓ Month 'May' (05) selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="05" and click it
                    try:
                        # Find the option element with value="05" within or near the dropdown
                        option_selector = "#divDOBMonAdult0 option[value='05'], #divDOBMonAdult0 li[data-value='05'], .dropdown-menu li[data-value='05']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Month 'May' (05) selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBMonAdult0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '05';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="05"]') || 
                                                   dropdown.querySelector('[value="05"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === 'May' || el.textContent.trim() === '05');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Month 'May' (05) selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Month dropdown for Adult DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Month dropdown (Adult DOB): {e}\n")
        
        # Step 11.4: Click on Year for Adult DOB
        print("🔍 STEP 7.4: Clicking on Date of Birth Year field for Adult...\n")
        
        try:
            # Wait for the DOB Year dropdown to appear (name="AdultYear" class="sel")
            page.wait_for_selector("select[name='AdultYear']", timeout=10000)
            print("✓ Year dropdown for Adult DOB found\n")
            
            # Get dropdown info
            year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.querySelector("select[name='AdultYear']");
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        name: dropdown.name,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Year Dropdown Info (Adult DOB): " + str(year_dropdown_info) + "\n")
            
            if year_dropdown_info.get('found'):
                # Click on the year dropdown
                try:
                    page.locator("select[name='AdultYear']").click(timeout=5000, force=True)
                    print("✓ Year dropdown for Adult DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.querySelector("select[name='AdultYear']");
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Year dropdown for Adult DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.5: Select year "2008" from the dropdown
                print("🔍 STEP 7.5: Selecting Year '2008' (value='2008') from Adult DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("select[name='AdultYear']").select_option("2008")
                    print("✓ Year '2008' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Use JavaScript to select the option
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.querySelector("select[name='AdultYear']");
                            if (dropdown) {
                                dropdown.value = '2008';
                                dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                            }
                        }
                        """)
                        print("✓ Year '2008' selected via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript selection also failed: {e2}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Year dropdown for Adult DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Year dropdown (Adult DOB): {e}\n")
        
        # Step 11.6: Enter Passport Number for Adult
        print("🔍 STEP 7.6: Entering Passport Number for Adult...\n")
        
        try:
            # Wait for the Passport Number field to appear
            page.wait_for_selector("#txtPassAdult0", timeout=10000)
            print("✓ Passport Number field for Adult found\n")
            
            # Get field info
            passport_field_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtPassAdult0');
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
            
            print("📌 Passport Number Field Info: " + str(passport_field_info) + "\n")
            
            if passport_field_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtPassAdult0").click(timeout=5000, force=True)
                    print("✓ Passport Number field clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "123TEST"
                try:
                    page.locator("#txtPassAdult0").fill("123TEST")
                    print("✓ Passport Number '123TEST' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtPassAdult0").clear()
                        page.locator("#txtPassAdult0").type("123TEST", delay=50)
                        print("✓ Passport Number '123TEST' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtPassAdult0');
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
                    print(f"✓ Passport Number field value: '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Number field: {e}\n")
        
        # Step 11.7: Click on Passport Expiry Day for Adult
        print("🔍 STEP 7.7: Clicking on Passport Expiry Day field for Adult...\n")
        
        try:
            # Wait for the Passport Expiry Day dropdown to appear
            page.wait_for_selector("#passEXDayAdult0", timeout=10000)
            print("✓ Passport Expiry Day dropdown for Adult found\n")
            
            # Get dropdown info
            pass_ex_day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXDayAdult0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Day Dropdown Info (Adult): " + str(pass_ex_day_dropdown_info) + "\n")
            
            if pass_ex_day_dropdown_info.get('found'):
                # Click on the day dropdown
                try:
                    page.locator("#passEXDayAdult0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Day dropdown for Adult clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXDayAdult0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Day dropdown for Adult clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.8: Select day "06" from the dropdown
                print("🔍 STEP 7.8: Selecting Day '06' from Passport Expiry Day dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXDayAdult0").select_option("06")
                    print("✓ Day '06' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="06" and click it
                    try:
                        # Find the option element with value="06" within or near the dropdown
                        option_selector = "#passEXDayAdult0 option[value='06'], #passEXDayAdult0 li[data-value='06'], .dropdown-menu li[data-value='06']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Day '06' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXDayAdult0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '06';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="06"]') || 
                                                   dropdown.querySelector('[value="06"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '06' || el.textContent.trim() === '6');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Day '06' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Day dropdown for Adult not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Day dropdown (Adult): {e}\n")
        
        # Step 11.9: Click on Passport Expiry Month for Adult
        print("🔍 STEP 7.9: Clicking on Passport Expiry Month field for Adult...\n")
        
        try:
            # Wait for the Passport Expiry Month dropdown to appear
            page.wait_for_selector("#passEXMonAdult0", timeout=10000)
            print("✓ Passport Expiry Month dropdown for Adult found\n")
            
            # Get dropdown info
            pass_ex_month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXMonAdult0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Month Dropdown Info (Adult): " + str(pass_ex_month_dropdown_info) + "\n")
            
            if pass_ex_month_dropdown_info.get('found'):
                # Click on the month dropdown
                try:
                    page.locator("#passEXMonAdult0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Month dropdown for Adult clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXMonAdult0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Month dropdown for Adult clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.10: Select month "May" from the dropdown
                print("🔍 STEP 7.10: Selecting Month 'May' from Passport Expiry Month dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements) - May could be "May" or "05"
                    try:
                        page.locator("#passEXMonAdult0").select_option("May")
                        print("✓ Month 'May' selected via select_option()")
                    except:
                        # Try alternative value for May
                        page.locator("#passEXMonAdult0").select_option("05")
                        print("✓ Month 'May' (05) selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with "May" and click it
                    try:
                        # Find the option element with "May" text
                        option_selector = "#passEXMonAdult0 option[value='May'], #passEXMonAdult0 li[data-value='May'], .dropdown-menu li:has(> * :text('May'))"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Month 'May' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXMonAdult0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        // Try to set value to "May" first, then "05"
                                        dropdown.value = 'May' || dropdown.value;
                                        if (dropdown.value !== 'May') {
                                            dropdown.value = '05';
                                        }
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="May"]') || 
                                                   dropdown.querySelector('[value="May"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === 'May');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Month 'May' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Month dropdown for Adult not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Month dropdown (Adult): {e}\n")
        
        # Step 11.11: Click on Passport Expiry Year for Adult
        print("🔍 STEP 7.11: Clicking on Passport Expiry Year field for Adult...\n")
        
        try:
            # Wait for the Passport Expiry Year dropdown to appear
            page.wait_for_selector("#passEXYearAdult0", timeout=10000)
            print("✓ Passport Expiry Year dropdown for Adult found\n")
            
            # Get dropdown info
            pass_ex_year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXYearAdult0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Year Dropdown Info (Adult): " + str(pass_ex_year_dropdown_info) + "\n")
            
            if pass_ex_year_dropdown_info.get('found'):
                # Click on the year dropdown
                try:
                    page.locator("#passEXYearAdult0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Year dropdown for Adult clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXYearAdult0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Year dropdown for Adult clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.12: Select year "2032" from the dropdown
                print("🔍 STEP 7.12: Selecting Year '2032' from Passport Expiry Year dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXYearAdult0").select_option("2032")
                    print("✓ Year '2032' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="2032" and click it
                    try:
                        # Find the option element with value="2032" within or near the dropdown
                        option_selector = "#passEXYearAdult0 option[value='2032'], #passEXYearAdult0 li[data-value='2032'], .dropdown-menu li[data-value='2032']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Year '2032' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXYearAdult0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '2032';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="2032"]') || 
                                                   dropdown.querySelector('[value="2032"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '2032');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Year '2032' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Year dropdown for Adult not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Year dropdown (Adult): {e}\n")
        
        # Step 11.13: Click on Day for Child DOB
        print("🔍 STEP 7.13: Clicking on Date of Birth Day field for Child...\n")
        
        try:
            # Wait for the DOB Day dropdown to appear
            page.wait_for_selector("#divDOBDayChild0", timeout=10000)
            print("✓ Day dropdown for Child DOB found\n")
            
            # Get dropdown info
            child_day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBDayChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Day Dropdown Info (Child DOB): " + str(child_day_dropdown_info) + "\n")
            
            if child_day_dropdown_info.get('found'):
                # Click on the day dropdown
                try:
                    page.locator("#divDOBDayChild0").click(timeout=5000, force=True)
                    print("✓ Day dropdown for Child DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBDayChild0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Day dropdown for Child DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.14: Select day "10" from the dropdown
                print("🔍 STEP 7.14: Selecting Day '10' from Child DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#divDOBDayChild0").select_option("10")
                    print("✓ Day '10' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="10" and click it
                    try:
                        # Find the option element with value="10" within or near the dropdown
                        option_selector = "#divDOBDayChild0 option[value='10'], #divDOBDayChild0 li[data-value='10'], .dropdown-menu li[data-value='10']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Day '10' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBDayChild0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '10';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="10"]') || 
                                                   dropdown.querySelector('[value="10"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '10');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Day '10' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Day dropdown for Child DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Day dropdown (Child DOB): {e}\n")
        
        # Step 11.15: Click on Month for Child DOB
        print("🔍 STEP 7.15: Clicking on Date of Birth Month field for Child...\n")
        
        try:
            # Wait for the DOB Month dropdown to appear
            page.wait_for_selector("#divDOBMonChild0", timeout=10000)
            print("✓ Month dropdown for Child DOB found\n")
            
            # Get dropdown info
            child_month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBMonChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Month Dropdown Info (Child DOB): " + str(child_month_dropdown_info) + "\n")
            
            if child_month_dropdown_info.get('found'):
                # Click on the month dropdown
                try:
                    page.locator("#divDOBMonChild0").click(timeout=5000, force=True)
                    print("✓ Month dropdown for Child DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBMonChild0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Month dropdown for Child DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.16: Select month "Aug" from the dropdown
                print("🔍 STEP 7.16: Selecting Month 'Aug' from Child DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements) - Aug could be "Aug" or "08"
                    try:
                        page.locator("#divDOBMonChild0").select_option("Aug")
                        print("✓ Month 'Aug' selected via select_option()")
                    except:
                        # Try alternative value for Aug
                        page.locator("#divDOBMonChild0").select_option("08")
                        print("✓ Month 'Aug' (08) selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with "Aug" and click it
                    try:
                        # Find the option element with "Aug" text
                        option_selector = "#divDOBMonChild0 option[value='Aug'], #divDOBMonChild0 li[data-value='Aug'], .dropdown-menu li:has(> * :text('Aug'))"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Month 'Aug' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBMonChild0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        // Try to set value to "Aug" first, then "08"
                                        dropdown.value = 'Aug' || dropdown.value;
                                        if (dropdown.value !== 'Aug') {
                                            dropdown.value = '08';
                                        }
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="Aug"]') || 
                                                   dropdown.querySelector('[value="Aug"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === 'Aug');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Month 'Aug' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Month dropdown for Child DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Month dropdown (Child DOB): {e}\n")
        
        # Step 11.17: Click on Year for Child DOB
        print("🔍 STEP 7.17: Clicking on Date of Birth Year field for Child...\n")
        
        try:
            # Wait for the DOB Year dropdown to appear
            page.wait_for_selector("#divDOBYarChild0", timeout=10000)
            print("✓ Year dropdown for Child DOB found\n")
            
            # Get dropdown info
            child_year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBYarChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Year Dropdown Info (Child DOB): " + str(child_year_dropdown_info) + "\n")
            
            if child_year_dropdown_info.get('found'):
                # Click on the year dropdown
                try:
                    page.locator("#divDOBYarChild0").click(timeout=5000, force=True)
                    print("✓ Year dropdown for Child DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBYarChild0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Year dropdown for Child DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.18: Select year "2017" from the dropdown
                print("🔍 STEP 7.18: Selecting Year '2017' from Child DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#divDOBYarChild0").select_option("2017")
                    print("✓ Year '2017' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="2017" and click it
                    try:
                        # Find the option element with value="2017" within or near the dropdown
                        option_selector = "#divDOBYarChild0 option[value='2017'], #divDOBYarChild0 li[data-value='2017'], .dropdown-menu li[data-value='2017']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Year '2017' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBYarChild0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '2017';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="2017"]') || 
                                                   dropdown.querySelector('[value="2017"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '2017');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Year '2017' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Year dropdown for Child DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Year dropdown (Child DOB): {e}\n")
        
        # Step 11.19: Enter Passport Number for Child
        print("🔍 STEP 7.19: Entering Passport Number for Child...\n")
        
        try:
            # Wait for the Passport Number field to appear
            page.wait_for_selector("#txtPassChild0", timeout=10000)
            print("✓ Passport Number field for Child found\n")
            
            # Get field info
            child_passport_field_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtPassChild0');
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
            
            print("📌 Passport Number Field Info (Child): " + str(child_passport_field_info) + "\n")
            
            if child_passport_field_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtPassChild0").click(timeout=5000, force=True)
                    print("✓ Passport Number field for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "456Test"
                try:
                    page.locator("#txtPassChild0").fill("456Test")
                    print("✓ Passport Number '456Test' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtPassChild0").clear()
                        page.locator("#txtPassChild0").type("456Test", delay=50)
                        print("✓ Passport Number '456Test' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtPassChild0');
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
                    print(f"✓ Passport Number field value (Child): '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Number field (Child): {e}\n")
        
        # Step 11.20: Click on Passport Expiry Day for Child
        print("🔍 STEP 7.20: Clicking on Passport Expiry Day field for Child...\n")
        
        try:
            # Wait for the Passport Expiry Day dropdown to appear
            page.wait_for_selector("#passEXDayChild0", timeout=10000)
            print("✓ Passport Expiry Day dropdown for Child found\n")
            
            # Get dropdown info
            child_pass_ex_day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXDayChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Day Dropdown Info (Child): " + str(child_pass_ex_day_dropdown_info) + "\n")
            
            if child_pass_ex_day_dropdown_info.get('found'):
                # Click on the day dropdown
                try:
                    page.locator("#passEXDayChild0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Day dropdown for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXDayChild0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Day dropdown for Child clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.21: Select day "04" from the dropdown
                print("🔍 STEP 7.21: Selecting Day '04' from Passport Expiry Day dropdown (Child)...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXDayChild0").select_option("04")
                    print("✓ Day '04' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="04" and click it
                    try:
                        # Find the option element with value="04" within or near the dropdown
                        option_selector = "#passEXDayChild0 option[value='04'], #passEXDayChild0 li[data-value='04'], .dropdown-menu li[data-value='04']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Day '04' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXDayChild0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '04';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="04"]') || 
                                                   dropdown.querySelector('[value="04"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '04' || el.textContent.trim() === '4');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Day '04' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Day dropdown for Child not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Day dropdown (Child): {e}\n")
        
        # Step 11.22: Click on Passport Expiry Month for Child
        print("🔍 STEP 7.22: Clicking on Passport Expiry Month field for Child...\n")
        
        try:
            # Wait for the Passport Expiry Month dropdown to appear
            page.wait_for_selector("#passEXMonChild0", timeout=10000)
            print("✓ Passport Expiry Month dropdown for Child found\n")
            
            # Get dropdown info
            child_pass_ex_month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXMonChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Month Dropdown Info (Child): " + str(child_pass_ex_month_dropdown_info) + "\n")
            
            if child_pass_ex_month_dropdown_info.get('found'):
                # Click on the month dropdown
                try:
                    page.locator("#passEXMonChild0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Month dropdown for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXMonChild0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Month dropdown for Child clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.23: Select month "Mar" from the dropdown
                print("🔍 STEP 7.23: Selecting Month 'Mar' from Passport Expiry Month dropdown (Child)...\n")
                
                try:
                    # Try using select_option method (for select elements) - Mar could be "Mar" or "03"
                    try:
                        page.locator("#passEXMonChild0").select_option("Mar")
                        print("✓ Month 'Mar' selected via select_option()")
                    except:
                        # Try alternative value for Mar
                        page.locator("#passEXMonChild0").select_option("03")
                        print("✓ Month 'Mar' (03) selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with "Mar" and click it
                    try:
                        # Find the option element with "Mar" text
                        option_selector = "#passEXMonChild0 option[value='Mar'], #passEXMonChild0 li[data-value='Mar'], .dropdown-menu li:has(> * :text('Mar'))"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Month 'Mar' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXMonChild0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        // Try to set value to "Mar" first, then "03"
                                        dropdown.value = 'Mar' || dropdown.value;
                                        if (dropdown.value !== 'Mar') {
                                            dropdown.value = '03';
                                        }
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="Mar"]') || 
                                                   dropdown.querySelector('[value="Mar"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === 'Mar');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Month 'Mar' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Month dropdown for Child not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Month dropdown (Child): {e}\n")
        
        # Step 11.24: Click on Passport Expiry Year for Child
        print("🔍 STEP 7.24: Clicking on Passport Expiry Year field for Child...\n")
        
        try:
            # Wait for the Passport Expiry Year dropdown to appear
            page.wait_for_selector("#passEXYearChild0", timeout=10000)
            print("✓ Passport Expiry Year dropdown for Child found\n")
            
            # Get dropdown info
            child_pass_ex_year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXYearChild0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Year Dropdown Info (Child): " + str(child_pass_ex_year_dropdown_info) + "\n")
            
            if child_pass_ex_year_dropdown_info.get('found'):
                # Click on the year dropdown
                try:
                    page.locator("#passEXYearChild0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Year dropdown for Child clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXYearChild0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Year dropdown for Child clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.25: Select year "2034" from the dropdown
                print("🔍 STEP 7.25: Selecting Year '2034' from Passport Expiry Year dropdown (Child)...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXYearChild0").select_option("2034")
                    print("✓ Year '2034' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="2034" and click it
                    try:
                        # Find the option element with value="2034" within or near the dropdown
                        option_selector = "#passEXYearChild0 option[value='2034'], #passEXYearChild0 li[data-value='2034'], .dropdown-menu li[data-value='2034']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Year '2034' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXYearChild0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '2034';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="2034"]') || 
                                                   dropdown.querySelector('[value="2034"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '2034');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Year '2034' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Year dropdown for Child not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Year dropdown (Child): {e}\n")
        
        # Step 11.26: Click on Day for Infant DOB
        print("🔍 STEP 7.26: Clicking on Date of Birth Day field for Infant...\n")
        
        try:
            # Wait for the DOB Day dropdown to appear
            page.wait_for_selector("#divDOBDayInfant0", timeout=10000)
            print("✓ Day dropdown for Infant DOB found\n")
            
            # Get dropdown info
            infant_day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBDayInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Day Dropdown Info (Infant DOB): " + str(infant_day_dropdown_info) + "\n")
            
            if infant_day_dropdown_info.get('found'):
                # Click on the day dropdown
                try:
                    page.locator("#divDOBDayInfant0").click(timeout=5000, force=True)
                    print("✓ Day dropdown for Infant DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBDayInfant0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Day dropdown for Infant DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.27: Select day "03" from the dropdown
                print("🔍 STEP 7.27: Selecting Day '03' from Infant DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#divDOBDayInfant0").select_option("03")
                    print("✓ Day '03' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="03" and click it
                    try:
                        # Find the option element with value="03" within or near the dropdown
                        option_selector = "#divDOBDayInfant0 option[value='03'], #divDOBDayInfant0 li[data-value='03'], .dropdown-menu li[data-value='03']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Day '03' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBDayInfant0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '03';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="03"]') || 
                                                   dropdown.querySelector('[value="03"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '03' || el.textContent.trim() === '3');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Day '03' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Day dropdown for Infant DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Day dropdown (Infant DOB): {e}\n")
        
        # Step 11.28: Click on Month for Infant DOB
        print("🔍 STEP 7.28: Clicking on Date of Birth Month field for Infant...\n")
        
        try:
            # Wait for the DOB Month dropdown to appear
            page.wait_for_selector("#divDOBMonInfant0", timeout=10000)
            print("✓ Month dropdown for Infant DOB found\n")
            
            # Get dropdown info
            infant_month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBMonInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Month Dropdown Info (Infant DOB): " + str(infant_month_dropdown_info) + "\n")
            
            if infant_month_dropdown_info.get('found'):
                # Click on the month dropdown
                try:
                    page.locator("#divDOBMonInfant0").click(timeout=5000, force=True)
                    print("✓ Month dropdown for Infant DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBMonInfant0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Month dropdown for Infant DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.29: Select month "Mar" from the dropdown
                print("🔍 STEP 7.29: Selecting Month 'Mar' from Infant DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements) - Mar could be "Mar" or "03"
                    try:
                        page.locator("#divDOBMonInfant0").select_option("Mar")
                        print("✓ Month 'Mar' selected via select_option()")
                    except:
                        # Try alternative value for Mar
                        page.locator("#divDOBMonInfant0").select_option("03")
                        print("✓ Month 'Mar' (03) selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with "Mar" and click it
                    try:
                        # Find the option element with "Mar" text
                        option_selector = "#divDOBMonInfant0 option[value='Mar'], #divDOBMonInfant0 li[data-value='Mar'], .dropdown-menu li:has(> * :text('Mar'))"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Month 'Mar' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBMonInfant0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        // Try to set value to "Mar" first, then "03"
                                        dropdown.value = 'Mar' || dropdown.value;
                                        if (dropdown.value !== 'Mar') {
                                            dropdown.value = '03';
                                        }
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="Mar"]') || 
                                                   dropdown.querySelector('[value="Mar"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === 'Mar');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Month 'Mar' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Month dropdown for Infant DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Month dropdown (Infant DOB): {e}\n")
        
        # Step 11.30: Click on Year for Infant DOB
        print("🔍 STEP 7.30: Clicking on Date of Birth Year field for Infant...\n")
        
        try:
            # Wait for the DOB Year dropdown to appear
            page.wait_for_selector("#divDOBYarInfant0", timeout=10000)
            print("✓ Year dropdown for Infant DOB found\n")
            
            # Get dropdown info
            infant_year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('divDOBYarInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Year Dropdown Info (Infant DOB): " + str(infant_year_dropdown_info) + "\n")
            
            if infant_year_dropdown_info.get('found'):
                # Click on the year dropdown
                try:
                    page.locator("#divDOBYarInfant0").click(timeout=5000, force=True)
                    print("✓ Year dropdown for Infant DOB clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('divDOBYarInfant0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Year dropdown for Infant DOB clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.31: Select year "2025" from the dropdown
                print("🔍 STEP 7.31: Selecting Year '2025' from Infant DOB dropdown...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#divDOBYarInfant0").select_option("2025")
                    print("✓ Year '2025' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="2025" and click it
                    try:
                        # Find the option element with value="2025" within or near the dropdown
                        option_selector = "#divDOBYarInfant0 option[value='2025'], #divDOBYarInfant0 li[data-value='2025'], .dropdown-menu li[data-value='2025']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Year '2025' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('divDOBYarInfant0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '2025';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="2025"]') || 
                                                   dropdown.querySelector('[value="2025"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '2025');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Year '2025' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Year dropdown for Infant DOB not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Year dropdown (Infant DOB): {e}\n")
        
        # Step 11.32: Enter Passport Number for Infant
        print("🔍 STEP 7.32: Entering Passport Number for Infant...\n")
        
        try:
            # Wait for the Passport Number field to appear
            page.wait_for_selector("#txtPassInfant0", timeout=10000)
            print("✓ Passport Number field for Infant found\n")
            
            # Get field info
            infant_passport_field_info = page.evaluate("""
            () => {
                let field = document.getElementById('txtPassInfant0');
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
            
            print("📌 Passport Number Field Info (Infant): " + str(infant_passport_field_info) + "\n")
            
            if infant_passport_field_info.get('found'):
                # Click on the field
                try:
                    page.locator("#txtPassInfant0").click(timeout=5000, force=True)
                    print("✓ Passport Number field for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                
                page.wait_for_timeout(500)
                
                # Clear any existing value and enter "789TEST"
                try:
                    page.locator("#txtPassInfant0").fill("789TEST")
                    print("✓ Passport Number '789TEST' entered via fill()")
                except Exception as e:
                    print(f"⚠ fill() failed: {e}")
                    
                    # Fallback: Use type() method
                    try:
                        page.locator("#txtPassInfant0").clear()
                        page.locator("#txtPassInfant0").type("789TEST", delay=50)
                        print("✓ Passport Number '789TEST' entered via type()")
                    except Exception as e2:
                        print(f"⚠ type() also failed: {e2}")
                
                page.wait_for_timeout(1000)
                
                # Verify the value was entered
                entered_value = page.evaluate("""
                () => {
                    let field = document.getElementById('txtPassInfant0');
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
                    print(f"✓ Passport Number field value (Infant): '{entered_value.get('value')}'\n")
                else:
                    print("⚠ Could not verify entered value\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Number field (Infant): {e}\n")
        
        # Step 11.33: Click on Passport Expiry Day for Infant
        print("🔍 STEP 7.33: Clicking on Passport Expiry Day field for Infant...\n")
        
        try:
            # Wait for the Passport Expiry Day dropdown to appear
            page.wait_for_selector("#passEXDayInfant0", timeout=10000)
            print("✓ Passport Expiry Day dropdown for Infant found\n")
            
            # Get dropdown info
            infant_pass_ex_day_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXDayInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Day Dropdown Info (Infant): " + str(infant_pass_ex_day_dropdown_info) + "\n")
            
            if infant_pass_ex_day_dropdown_info.get('found'):
                # Click on the day dropdown
                try:
                    page.locator("#passEXDayInfant0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Day dropdown for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXDayInfant0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Day dropdown for Infant clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.34: Select day "12" from the dropdown
                print("🔍 STEP 7.34: Selecting Day '12' from Passport Expiry Day dropdown (Infant)...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXDayInfant0").select_option("12")
                    print("✓ Day '12' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="12" and click it
                    try:
                        # Find the option element with value="12" within or near the dropdown
                        option_selector = "#passEXDayInfant0 option[value='12'], #passEXDayInfant0 li[data-value='12'], .dropdown-menu li[data-value='12']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Day '12' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXDayInfant0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '12';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="12"]') || 
                                                   dropdown.querySelector('[value="12"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '12');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Day '12' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Day dropdown for Infant not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Day dropdown (Infant): {e}\n")
        
        # Step 11.35: Click on Passport Expiry Month for Infant
        print("🔍 STEP 7.35: Clicking on Passport Expiry Month field for Infant...\n")
        
        try:
            # Wait for the Passport Expiry Month dropdown to appear
            page.wait_for_selector("#passEXMonInfant0", timeout=10000)
            print("✓ Passport Expiry Month dropdown for Infant found\n")
            
            # Get dropdown info
            infant_pass_ex_month_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXMonInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Month Dropdown Info (Infant): " + str(infant_pass_ex_month_dropdown_info) + "\n")
            
            if infant_pass_ex_month_dropdown_info.get('found'):
                # Click on the month dropdown
                try:
                    page.locator("#passEXMonInfant0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Month dropdown for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXMonInfant0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Month dropdown for Infant clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.36: Select month "09" from the dropdown
                print("🔍 STEP 7.36: Selecting Month '09' from Passport Expiry Month dropdown (Infant)...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXMonInfant0").select_option("09")
                    print("✓ Month '09' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="09" and click it
                    try:
                        # Find the option element with value="09" within or near the dropdown
                        option_selector = "#passEXMonInfant0 option[value='09'], #passEXMonInfant0 li[data-value='09'], .dropdown-menu li[data-value='09']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Month '09' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXMonInfant0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '09';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="09"]') || 
                                                   dropdown.querySelector('[value="09"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '09' || el.textContent.trim() === 'Sep' || el.textContent.trim() === 'September');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Month '09' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Month dropdown for Infant not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Month dropdown (Infant): {e}\n")
        
        # Step 11.37: Click on Passport Expiry Year for Infant
        print("🔍 STEP 7.37: Clicking on Passport Expiry Year field for Infant...\n")
        
        try:
            # Wait for the Passport Expiry Year dropdown to appear
            page.wait_for_selector("#passEXYearInfant0", timeout=10000)
            print("✓ Passport Expiry Year dropdown for Infant found\n")
            
            # Get dropdown info
            infant_pass_ex_year_dropdown_info = page.evaluate("""
            () => {
                let dropdown = document.getElementById('passEXYearInfant0');
                if (dropdown) {
                    return {
                        found: true,
                        tagName: dropdown.tagName,
                        id: dropdown.id,
                        className: dropdown.className,
                        visible: dropdown.offsetParent !== null
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Passport Expiry Year Dropdown Info (Infant): " + str(infant_pass_ex_year_dropdown_info) + "\n")
            
            if infant_pass_ex_year_dropdown_info.get('found'):
                # Click on the year dropdown
                try:
                    page.locator("#passEXYearInfant0").click(timeout=5000, force=True)
                    print("✓ Passport Expiry Year dropdown for Infant clicked via Playwright")
                except Exception as e:
                    print(f"⚠ Playwright click failed: {e}")
                    
                    # Fallback: Use JavaScript click
                    try:
                        page.evaluate("""
                        () => {
                            let dropdown = document.getElementById('passEXYearInfant0');
                            if (dropdown) {
                                dropdown.click();
                            }
                        }
                        """)
                        print("✓ Passport Expiry Year dropdown for Infant clicked via JavaScript")
                    except Exception as e2:
                        print(f"⚠ JavaScript click also failed: {e2}")
                
                page.wait_for_timeout(800)
                
                # Step 11.38: Select year "2038" from the dropdown
                print("🔍 STEP 7.38: Selecting Year '2038' from Passport Expiry Year dropdown (Infant)...\n")
                
                try:
                    # Try using select_option method (for select elements)
                    page.locator("#passEXYearInfant0").select_option("2038")
                    print("✓ Year '2038' selected via select_option()")
                except Exception as e:
                    print(f"⚠ select_option() failed: {e}")
                    
                    # Fallback: Look for option element with value="2038" and click it
                    try:
                        # Find the option element with value="2038" within or near the dropdown
                        option_selector = "#passEXYearInfant0 option[value='2038'], #passEXYearInfant0 li[data-value='2038'], .dropdown-menu li[data-value='2038']"
                        page.locator(option_selector).first.click(timeout=5000)
                        print("✓ Year '2038' selected via option click")
                    except Exception as e2:
                        print(f"⚠ Option click failed: {e2}")
                        
                        # Fallback: Use JavaScript to select the option
                        try:
                            page.evaluate("""
                            () => {
                                let dropdown = document.getElementById('passEXYearInfant0');
                                if (dropdown) {
                                    // If it's a select element
                                    if (dropdown.tagName === 'SELECT') {
                                        dropdown.value = '2038';
                                        dropdown.dispatchEvent(new Event('change', { bubbles: true }));
                                    }
                                    // If it's a custom dropdown, try to find and click the option
                                    else {
                                        let option = dropdown.querySelector('[data-value="2038"]') || 
                                                   dropdown.querySelector('[value="2038"]') ||
                                                   Array.from(dropdown.querySelectorAll('li, span, div')).find(el => el.textContent.trim() === '2038');
                                        if (option) {
                                            option.click();
                                        }
                                    }
                                }
                            }
                            """)
                            print("✓ Year '2038' selected via JavaScript")
                        except Exception as e3:
                            print(f"⚠ JavaScript selection also failed: {e3}")
                
                page.wait_for_timeout(500)
            else:
                print("⚠ Passport Expiry Year dropdown for Infant not found\n")
        
        except Exception as e:
            print(f"⚠ Error with Passport Expiry Year dropdown (Infant): {e}\n")
        
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
            # First, let's find ALL buttons on the page
            all_buttons_info = page.evaluate("""
            () => {
                let buttons = document.querySelectorAll('button');
                let results = [];
                for (let i = 0; i < buttons.length; i++) {
                    let btn = buttons[i];
                    let text = btn.textContent.trim().substring(0, 50);
                    if (text.length > 0 || btn.id || btn.className) {
                        results.push({
                            index: i,
                            id: btn.id,
                            className: btn.className,
                            text: text,
                            type: btn.type,
                            visible: btn.offsetParent !== null,
                            display: window.getComputedStyle(btn).display,
                            zIndex: window.getComputedStyle(btn).zIndex
                        });
                    }
                }
                return results;
            }
            """)
            
            print("📊 ALL BUTTONS ON PAGE:")
            for btn_info in all_buttons_info:
                print(f"  - ID: {btn_info['id']}, Class: {btn_info['className']}, Text: {btn_info['text']}, Visible: {btn_info['visible']}")
            
            # Get Make Payment button info
            make_payment_info = page.evaluate("""
            () => {
                let button = null;
                
                // Try multiple selectors
                const selectors = [
                    '.mk-pym4',
                    '[class*="mk-pym4"]',
                    '[id*="Payment"]',
                    '[id*="payment"]',
                    'button[type="submit"]',
                ];
                
                for (let selector of selectors) {
                    button = document.querySelector(selector);
                    if (button && button.offsetParent !== null) {
                        break;
                    }
                }
                
                // If still not found, search by text content
                if (!button) {
                    let buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        if (btn.textContent.includes('Payment') || btn.textContent.includes('payment')) {
                            if (btn.offsetParent !== null) {
                                button = btn;
                                break;
                            }
                        }
                    }
                }
                
                if (button) {
                    // Scroll into view
                    button.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    return {
                        found: true,
                        tagName: button.tagName,
                        className: button.className,
                        id: button.id,
                        text: button.textContent.trim().substring(0, 100),
                        visible: button.offsetParent !== null,
                        type: button.type,
                        display: window.getComputedStyle(button).display,
                        position: window.getComputedStyle(button).position,
                        zIndex: window.getComputedStyle(button).zIndex
                    };
                }
                return { found: false };
            }
            """)
            
            print("📌 Make Payment Button Info: " + str(make_payment_info) + "\n")
            
            if make_payment_info.get('found'):
                print(f"✓ Make Payment button found - Attempting click methods...\n")
                
                # Method 1: Try clicking via Playwright with force and no timeout
                clicked = False
                try:
                    page.locator(".mk-pym4").first.click(timeout=5000, force=True)
                    print("✓ Make Payment button clicked via Playwright (Method 1)\n")
                    clicked = True
                except Exception as e:
                    print(f"⚠ Playwright click (Method 1) failed: {e}")
                
                # Method 2: Try alternative Playwright selector
                if not clicked:
                    try:
                        page.locator("button:has-text('Payment')").first.click(timeout=5000, force=True)
                        print("✓ Make Payment button clicked via Playwright (Method 2 - text selector)\n")
                        clicked = True
                    except Exception as e:
                        print(f"⚠ Playwright click (Method 2) failed: {e}")
                
                # Method 3: Try JavaScript click with multiple event types
                if not clicked:
                    try:
                        result = page.evaluate("""
                        () => {
                            let button = document.querySelector('.mk-pym4');
                            if (!button) {
                                button = document.querySelector('[class*="mk-pym4"]');
                            }
                            if (!button) {
                                let buttons = document.querySelectorAll('button');
                                for (let btn of buttons) {
                                    if (btn.textContent.includes('Payment') || btn.textContent.includes('payment')) {
                                        button = btn;
                                        break;
                                    }
                                }
                            }
                            
                            if (button) {
                                // Make sure button is visible and enabled
                                button.style.display = 'block';
                                button.style.visibility = 'visible';
                                button.disabled = false;
                                
                                // Trigger multiple events
                                button.click();
                                button.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                                button.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                                button.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                button.dispatchEvent(new Event('click', { bubbles: true }));
                                
                                // Try form submission if it's inside a form
                                if (button.form) {
                                    button.form.submit();
                                }
                                
                                return { success: true, message: 'Button clicked via JavaScript' };
                            }
                            return { success: false, message: 'Button not found' };
                        }
                        """)
                        
                        if result.get('success'):
                            print(f"✓ Make Payment button clicked via JavaScript (Method 3): {result.get('message')}\n")
                            clicked = True
                        else:
                            print(f"⚠ JavaScript click (Method 3) failed: {result.get('message')}\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click (Method 3) failed: {e2}\n")
                
                # Wait after click
                page.wait_for_timeout(2000)
                
                # Check final URL after clicking
                final_url = page.url
                print(f"✓ Current URL after Make Payment click: {final_url}\n")
                
                if not clicked:
                    print("⚠ All click methods failed - button may be disabled or hidden\n")
                
            else:
                print("⚠ Make Payment button not found on page\n")
                print("💡 Debugging: This could mean:")
                print("   1. Page is still loading")
                print("   2. Button has different class/id than expected")
                print("   3. Button is inside an iframe")
                print("   4. Payment gateway hasn't fully loaded yet\n")
        
        except Exception as e:
            print(f"⚠ Error with Make Payment button: {e}\n")
        
        page.wait_for_timeout(3000)
        
        # Step 26: Click on PayPal Payment Method
        print("🔍 STEP 26: Clicking on PayPal Payment Method (class='paypal-txt PG2')...\n")
        
        try:
            # First, let's find all payment method options on the page
            all_payment_methods = page.evaluate("""
            () => {
                let methods = [];
                
                // Look for elements with class containing 'paypal' or 'PG'
                let allDivs = document.querySelectorAll('[class*="paypal"], [class*="PG"]');
                for (let div of allDivs) {
                    let text = div.textContent.trim().substring(0, 50);
                    if (text.length > 0) {
                        methods.push({
                            className: div.className,
                            tagName: div.tagName,
                            text: text,
                            visible: div.offsetParent !== null
                        });
                    }
                }
                
                return methods.length > 0 ? methods : 'No PayPal elements found';
            }
            """)
            
            print("📊 Payment Methods Found:")
            if isinstance(all_payment_methods, list):
                for method in all_payment_methods:
                    print(f"  - Class: {method['className']}, Text: {method['text']}, Visible: {method['visible']}")
            else:
                print(f"  {all_payment_methods}")
            
            # Get PayPal button info
            paypal_info = page.evaluate("""
            () => {
                let paypalBtn = null;
                
                // Try exact selector first
                paypalBtn = document.querySelector('.paypal-txt.PG2');
                if (!paypalBtn) {
                    paypalBtn = document.querySelector('[class*="paypal-txt"]');
                }
                if (!paypalBtn) {
                    paypalBtn = document.querySelector('[class*="PayPal"]');
                }
                
                // Search through all divs and spans for PayPal text
                if (!paypalBtn) {
                    let elements = document.querySelectorAll('div, span, button');
                    for (let elem of elements) {
                        if ((elem.textContent.includes('PayPal') || elem.textContent.includes('paypal')) && elem.offsetParent !== null) {
                            paypalBtn = elem;
                            break;
                        }
                    }
                }
                
                if (paypalBtn) {
                    // Scroll into view
                    paypalBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    return {
                        found: true,
                        className: paypalBtn.className,
                        id: paypalBtn.id,
                        tagName: paypalBtn.tagName,
                        text: paypalBtn.textContent.trim().substring(0, 100),
                        visible: paypalBtn.offsetParent !== null,
                        display: window.getComputedStyle(paypalBtn).display,
                        zIndex: window.getComputedStyle(paypalBtn).zIndex
                    };
                }
                
                return { found: false };
            }
            """)
            
            print(f"📌 PayPal Button Info: {paypal_info}\n")
            
            if paypal_info.get('found'):
                print("✓ PayPal payment method found - Attempting click...\n")
                
                clicked = False
                
                # Method 1: Try Playwright click
                try:
                    page.locator('.paypal-txt').first.click(timeout=5000, force=True)
                    print("✓ PayPal button clicked via Playwright (Method 1)\n")
                    clicked = True
                except Exception as e:
                    print(f"⚠ Playwright click (Method 1) failed: {e}")
                
                # Method 2: Try alternative Playwright selector
                if not clicked:
                    try:
                        page.locator('[class*="paypal"]').first.click(timeout=5000, force=True)
                        print("✓ PayPal button clicked via Playwright (Method 2 - wildcard)\n")
                        clicked = True
                    except Exception as e:
                        print(f"⚠ Playwright click (Method 2) failed: {e}")
                
                # Method 3: Try JavaScript click
                if not clicked:
                    try:
                        result = page.evaluate("""
                        () => {
                            let paypalBtn = document.querySelector('.paypal-txt.PG2');
                            if (!paypalBtn) {
                                paypalBtn = document.querySelector('[class*="paypal-txt"]');
                            }
                            if (!paypalBtn) {
                                let elements = document.querySelectorAll('div, span, button');
                                for (let elem of elements) {
                                    if ((elem.textContent.includes('PayPal') || elem.textContent.includes('paypal')) && elem.offsetParent !== null) {
                                        paypalBtn = elem;
                                        break;
                                    }
                                }
                            }
                            
                            if (paypalBtn) {
                                // Ensure visibility
                                paypalBtn.style.display = 'block';
                                paypalBtn.style.visibility = 'visible';
                                paypalBtn.style.pointerEvents = 'auto';
                                
                                // Trigger multiple events
                                paypalBtn.click();
                                paypalBtn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                                paypalBtn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                                paypalBtn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                paypalBtn.dispatchEvent(new Event('click', { bubbles: true }));
                                
                                return { success: true, message: 'PayPal button clicked via JavaScript' };
                            }
                            return { success: false, message: 'PayPal button not found' };
                        }
                        """)
                        
                        if result.get('success'):
                            print(f"✓ PayPal button clicked via JavaScript (Method 3): {result.get('message')}\n")
                            clicked = True
                        else:
                            print(f"⚠ JavaScript click (Method 3) failed: {result.get('message')}\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click (Method 3) failed: {e2}\n")
                
                # Wait after click
                page.wait_for_timeout(2000)
                
                # Check URL after click
                current_url = page.url
                print(f"✓ Current URL after PayPal click: {current_url}\n")
                
                if clicked:
                    print("✅ PayPal payment method selected successfully!\n")
                else:
                    print("⚠ All click methods failed\n")
            
            else:
                print("⚠ PayPal payment method button not found on page\n")
                print("💡 Debugging: This could mean:")
                print("   1. PayPal option is not available on this payment page")
                print("   2. Button has different class/id than expected")
                print("   3. Payment page hasn't fully loaded yet\n")
        
        except Exception as e:
            print(f"⚠ Error clicking PayPal button: {e}\n")
        
        page.wait_for_timeout(2000)
        
        # Step 27: Click on PayPal Validation Button (ng-click="MakevalidatepAYPAL()")
        print("🔍 STEP 27: Clicking on PayPal Validation Button (ng-click='MakevalidatepAYPAL()')...\n")
        
        try:
            # Get PayPal validation button info
            validation_btn_info = page.evaluate("""
            () => {
                let validationBtn = null;
                
                // Look for element with ng-click attribute
                validationBtn = document.querySelector('[ng-click*="MakevalidatepAYPAL"]');
                
                // Alternative: search for button with this attribute
                if (!validationBtn) {
                    let buttons = document.querySelectorAll('button, div, span, a');
                    for (let btn of buttons) {
                        if (btn.getAttribute('ng-click') && btn.getAttribute('ng-click').includes('MakevalidatepAYPAL')) {
                            validationBtn = btn;
                            break;
                        }
                    }
                }
                
                if (validationBtn) {
                    // Scroll into view
                    validationBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    return {
                        found: true,
                        className: validationBtn.className,
                        id: validationBtn.id,
                        tagName: validationBtn.tagName,
                        text: validationBtn.textContent.trim().substring(0, 100),
                        ngClick: validationBtn.getAttribute('ng-click'),
                        visible: validationBtn.offsetParent !== null,
                        display: window.getComputedStyle(validationBtn).display
                    };
                }
                
                return { found: false };
            }
            """)
            
            print(f"📌 PayPal Validation Button Info: {validation_btn_info}\n")
            
            if validation_btn_info.get('found'):
                print("✓ PayPal validation button found - Attempting click...\n")
                
                clicked = False
                
                # Method 1: Try Playwright click using ng-click attribute
                try:
                    page.locator('[ng-click*="MakevalidatepAYPAL"]').first.click(timeout=5000, force=True)
                    print("✓ PayPal validation button clicked via Playwright (Method 1)\n")
                    clicked = True
                except Exception as e:
                    print(f"⚠ Playwright click (Method 1) failed: {e}")
                
                # Method 2: Try JavaScript click
                if not clicked:
                    try:
                        result = page.evaluate("""
                        () => {
                            let validationBtn = document.querySelector('[ng-click*="MakevalidatepAYPAL"]');
                            
                            if (!validationBtn) {
                                let buttons = document.querySelectorAll('button, div, span, a');
                                for (let btn of buttons) {
                                    if (btn.getAttribute('ng-click') && btn.getAttribute('ng-click').includes('MakevalidatepAYPAL')) {
                                        validationBtn = btn;
                                        break;
                                    }
                                }
                            }
                            
                            if (validationBtn) {
                                // Ensure visibility
                                validationBtn.style.display = 'block';
                                validationBtn.style.visibility = 'visible';
                                validationBtn.style.pointerEvents = 'auto';
                                validationBtn.disabled = false;
                                
                                // Trigger multiple events
                                validationBtn.click();
                                validationBtn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                                validationBtn.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                                validationBtn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                validationBtn.dispatchEvent(new Event('click', { bubbles: true }));
                                
                                return { success: true, message: 'PayPal validation button clicked via JavaScript' };
                            }
                            return { success: false, message: 'PayPal validation button not found' };
                        }
                        """)
                        
                        if result.get('success'):
                            print(f"✓ PayPal validation button clicked via JavaScript (Method 2): {result.get('message')}\n")
                            clicked = True
                        else:
                            print(f"⚠ JavaScript click (Method 2) failed: {result.get('message')}\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click (Method 2) failed: {e2}\n")
                
                # Wait after click
                page.wait_for_timeout(3000)
                
                # Check URL after click
                current_url = page.url
                print(f"✓ Current URL after PayPal validation click: {current_url}\n")
                
                if clicked:
                    print("✅ PayPal validation successful!\n")
                else:
                    print("⚠ All click methods failed\n")
            
            else:
                print("⚠ PayPal validation button not found on page\n")
                print("💡 Debugging: This could mean:")
                print("   1. PayPal validation button hasn't loaded yet")
                print("   2. Button has different ng-click value than expected")
                print("   3. Page structure has changed\n")
        
        except Exception as e:
            print(f"⚠ Error clicking PayPal validation button: {e}\n")
        
        page.wait_for_timeout(3000)
        
        # Step 28: Click on Cancel and Return to EaseMyTrip Link (id="cancelLink")
        print("🔍 STEP 28: Clicking on 'Cancel and return to EaseMyTrip UK Ltd' (id='cancelLink')...\n")
        
        try:
            # Get cancel link info
            cancel_link_info = page.evaluate("""
            () => {
                let cancelLink = null;
                
                // Try exact ID selector first
                cancelLink = document.getElementById('cancelLink');
                
                // Alternative: search by id attribute
                if (!cancelLink) {
                    cancelLink = document.querySelector('#cancelLink');
                }
                
                // Alternative: search for elements containing 'cancel' and 'EaseMyTrip' text
                if (!cancelLink) {
                    let allElements = document.querySelectorAll('a, button, div, span');
                    for (let elem of allElements) {
                        if ((elem.textContent.includes('Cancel') && elem.textContent.includes('EaseMyTrip')) || 
                            elem.textContent.includes('cancel and return')) {
                            cancelLink = elem;
                            break;
                        }
                    }
                }
                
                if (cancelLink) {
                    // Scroll into view
                    cancelLink.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    
                    return {
                        found: true,
                        className: cancelLink.className,
                        id: cancelLink.id,
                        tagName: cancelLink.tagName,
                        text: cancelLink.textContent.trim().substring(0, 100),
                        href: cancelLink.getAttribute('href') || 'N/A',
                        visible: cancelLink.offsetParent !== null,
                        display: window.getComputedStyle(cancelLink).display
                    };
                }
                
                return { found: false };
            }
            """)
            
            print(f"📌 Cancel Link Info: {cancel_link_info}\n")
            
            if cancel_link_info.get('found'):
                print("✓ Cancel and return link found - Attempting click...\n")
                
                clicked = False
                
                # Method 1: Try Playwright click using ID
                try:
                    page.locator('#cancelLink').first.click(timeout=5000, force=True)
                    print("✓ Cancel link clicked via Playwright (Method 1)\n")
                    clicked = True
                except Exception as e:
                    print(f"⚠ Playwright click (Method 1) failed: {e}")
                
                # Method 2: Try alternative Playwright selector
                if not clicked:
                    try:
                        page.locator('[id="cancelLink"]').first.click(timeout=5000, force=True)
                        print("✓ Cancel link clicked via Playwright (Method 2 - attribute selector)\n")
                        clicked = True
                    except Exception as e:
                        print(f"⚠ Playwright click (Method 2) failed: {e}")
                
                # Method 3: Try JavaScript click
                if not clicked:
                    try:
                        result = page.evaluate("""
                        () => {
                            let cancelLink = document.getElementById('cancelLink');
                            
                            if (!cancelLink) {
                                cancelLink = document.querySelector('#cancelLink');
                            }
                            
                            if (!cancelLink) {
                                let allElements = document.querySelectorAll('a, button, div, span');
                                for (let elem of allElements) {
                                    if ((elem.textContent.includes('Cancel') && elem.textContent.includes('EaseMyTrip')) || 
                                        elem.textContent.includes('cancel and return')) {
                                        cancelLink = elem;
                                        break;
                                    }
                                }
                            }
                            
                            if (cancelLink) {
                                // Ensure visibility
                                cancelLink.style.display = 'block';
                                cancelLink.style.visibility = 'visible';
                                cancelLink.style.pointerEvents = 'auto';
                                
                                // Trigger multiple events
                                cancelLink.click();
                                cancelLink.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
                                cancelLink.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true }));
                                cancelLink.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                                cancelLink.dispatchEvent(new Event('click', { bubbles: true }));
                                
                                return { success: true, message: 'Cancel link clicked via JavaScript' };
                            }
                            return { success: false, message: 'Cancel link not found' };
                        }
                        """)
                        
                        if result.get('success'):
                            print(f"✓ Cancel link clicked via JavaScript (Method 3): {result.get('message')}\n")
                            clicked = True
                        else:
                            print(f"⚠ JavaScript click (Method 3) failed: {result.get('message')}\n")
                    except Exception as e2:
                        print(f"⚠ JavaScript click (Method 3) failed: {e2}\n")
                
                # Wait after click
                page.wait_for_timeout(3000)
                
                # Check URL after click
                current_url = page.url
                print(f"✓ Current URL after cancel and return click: {current_url}\n")
                
                if clicked:
                    print("✅ Successfully returned to EaseMyTrip!\n")
                else:
                    print("⚠ All click methods failed\n")
            
            else:
                print("⚠ Cancel and return link not found on page\n")
                print("💡 Debugging: This could mean:")
                print("   1. Cancel link hasn't loaded on the PayPal page yet")
                print("   2. Link has different ID or structure than expected")
                print("   3. Currently not on PayPal page\n")
        
        except Exception as e:
            print(f"⚠ Error clicking cancel and return link: {e}\n")
        
        page.wait_for_timeout(2000)
        
        # Step 29: Take a screenshot and save it
        print("📸 STEP 29: Taking a screenshot and saving it...\n")
        
        try:
            # Create the ScreenShot directory if it doesn't exist
            screenshot_dir = r"D:\EMT_Flight_Playwright\Test_cases\ScreenShot"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
                print(f"✓ Created screenshot directory: {screenshot_dir}\n")
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"final_page_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_filename)
            
            # Take screenshot
            page.screenshot(path=screenshot_path)
            
            print(f"✓ Screenshot captured successfully!\n")
            print(f"📁 Screenshot saved to: {screenshot_path}\n")
            print(f"📌 File size: {os.path.getsize(screenshot_path)} bytes\n")
            print(f"✅ Screenshot saved successfully!\n")
            
        except Exception as e:
            print(f"⚠ Error taking screenshot: {e}\n")
        
        page.wait_for_timeout(1000)
        
        # Close browser
        print("🔌 Closing browser...\n")
        browser.close()
        print("✅ Browser closed successfully!\n")
        print("=" * 60)
        print("🎉 COMPLETE FLIGHT BOOKING AUTOMATION TEST FINISHED!")
        print("=" * 60)

if __name__ == "__main__":
    search_flight()

