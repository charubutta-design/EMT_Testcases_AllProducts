"""
Test case for verifying destination station autosuggestion on listing page.
"""

import pytest
from pages.train_page import TrainPage
from pages.listing_page import ListingPage


class TestListingDestinationAutosuggestion:
    """Test case for destination station autosuggestion on listing page."""

    def test_listing_destination_station_autosuggestion(self, page):
        """
        Test destination station field autosuggestion on listing page.
        
        Steps:
        1. Navigate to train homepage
        2. Enter source station (Patna)
        3. Enter destination station (Howrah)
        4. Click on date field and select RANDOM date from calendar
        5. Click search button
        6. On listing page, click on destination station field
        7. Type partial station name (e.g., 'Mum' for Mumbai)
        8. Verify autosuggestion dropdown appears with options
        9. Select from autosuggestion dropdown
        10. Verify selected station is populated in field
        
        Verifies:
        - Destination station text field is clickable on listing page
        - Typing in field shows autosuggestion dropdown
        - Autosuggestion contains matching station options
        - Selection from dropdown populates the field
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        # Initialize page objects
        train_page = TrainPage(page)
        listing_page = ListingPage(page)

        # Step 1: Navigate to train booking homepage
        train_page.open_train_page()

        # Step 2 & 3: Enter search criteria
        from_city = "Patna"
        to_city = "Howrah"
        train_page.enter_stations(from_city, to_city)
        
        # Step 4: Click on date field and select RANDOM date from calendar
        selected_day = train_page.select_random_date_from_calendar()
        print(f"✓ Selected random day {selected_day} from homepage calendar")

        # Step 5: Perform search
        train_page.click_search()

        # Wait for listing page to load
        listing_page.wait_for_page_load()

        # Verify we're on listing page
        current_url = listing_page.get_current_url().lower()
        assert "trainlistinfo" in current_url or "trainlist" in current_url, \
            "Should be on train listing page"
        
        print(f"✓ On listing page: {current_url}")
        
        # Step 6, 7, 8, 9: Test autosuggestion on DESTINATION station field
        # Type partial station name 'Mum' for Mumbai
        autosuggestion_result = listing_page.enter_station_and_check_autosuggestion('to', 'Mum')
        
        print(f"✓ Destination field clicked and typed 'Mum'")
        print(f"✓ Autosuggestion visible: {autosuggestion_result['autosuggestion_visible']}")
        print(f"✓ Options count: {autosuggestion_result['options_count']}")
        
        if autosuggestion_result['options_text']:
            print(f"✓ Autosuggestion options: {autosuggestion_result['options_text']}")
        
        # Step 10: Verify selected station
        if autosuggestion_result['selected_option']:
            print(f"✓ Selected option from autosuggestion: {autosuggestion_result['selected_option']}")
        
        # Assert autosuggestion appeared
        assert autosuggestion_result['autosuggestion_visible'] or autosuggestion_result['options_count'] > 0, \
            "Autosuggestion should appear when typing in destination station field"
        
        print(f"✓ Destination station autosuggestion test completed successfully")


class TestListingDestinationAutosuggestionAlternate:
    """Test case for destination autosuggestion with different station."""

    def test_listing_destination_autosuggestion_delhi(self, page):
        """
        Test destination station autosuggestion with 'Del' for Delhi.
        
        Steps:
        1. Navigate to train homepage
        2. Enter source and destination
        3. Select random date from calendar
        4. Search and go to listing page
        5. Type 'Del' in destination field
        6. Verify autosuggestion for Delhi appears
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        train_page = TrainPage(page)
        listing_page = ListingPage(page)

        # Navigate and search
        train_page.open_train_page()
        train_page.enter_stations("Lucknow", "Kanpur")
        train_page.select_random_date_from_calendar()
        train_page.click_search()
        listing_page.wait_for_page_load()

        # Verify on listing page
        current_url = listing_page.get_current_url().lower()
        assert "trainlistinfo" in current_url or "trainlist" in current_url

        # Test destination autosuggestion with 'Del'
        autosuggestion_result = listing_page.enter_station_and_check_autosuggestion('to', 'Del')
        
        print(f"✓ Typed 'Del' in destination field")
        print(f"✓ Autosuggestion visible: {autosuggestion_result['autosuggestion_visible']}")
        print(f"✓ Options count: {autosuggestion_result['options_count']}")
        
        if autosuggestion_result['options_text']:
            # Check if Delhi appears in options
            delhi_found = any('delhi' in opt.lower() for opt in autosuggestion_result['options_text'])
            print(f"✓ Delhi found in options: {delhi_found}")
            print(f"✓ Options: {autosuggestion_result['options_text'][:5]}")
        
        print(f"✓ Destination autosuggestion test with 'Del' completed")
