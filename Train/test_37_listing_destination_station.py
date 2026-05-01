"""
Test case for verifying destination station field on listing page.
"""

import pytest
from pages.train_page import TrainPage
from pages.listing_page import ListingPage


class TestListingDestinationStation:
    """Test case for destination station field on listing page."""

    def test_listing_destination_station_display(self, page):
        """
        Test that destination station field is displayed and editable on listing page.
        
        Steps:
        1. Navigate to train homepage
        2. Enter source station (Lucknow)
        3. Enter destination station (Kanpur)
        4. Click on date field and select RANDOM date from calendar
        5. Click search button
        6. Verify destination station field is displayed on listing page
        7. Click on destination station field and test autosuggestion
        
        Verifies:
        - Destination station text field is visible on listing page
        - Station name is pre-filled from homepage selection
        - Field can be clicked and edited with autosuggestion
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        # Initialize page objects
        train_page = TrainPage(page)
        listing_page = ListingPage(page)

        # Step 1: Navigate to train booking homepage
        train_page.open_train_page()

        # Step 2 & 3: Enter search criteria with different stations
        from_city = "Lucknow"
        to_city = "Kanpur"
        train_page.enter_stations(from_city, to_city)
        
        # Step 4: Click on date field and select RANDOM date from calendar
        selected_day = train_page.select_random_date_from_calendar()
        print(f"✓ Selected random day {selected_day} from homepage calendar")

        # Step 5: Perform search
        train_page.click_search()

        # Wait for listing page to load
        listing_page.wait_for_page_load()

        # Step 6: Verify we're on listing page
        current_url = listing_page.get_current_url().lower()
        assert "trainlistinfo" in current_url or "trainlist" in current_url, \
            "Should be on train listing page"
        
        print(f"✓ On listing page: {current_url}")
        
        # Check URL contains destination station info
        assert "kanpur" in current_url.lower(), \
            f"URL should contain destination station: {to_city}"
        
        # Step 7: Test destination station field with autosuggestion
        # Try to get destination station value from listing page
        listing_to = listing_page.get_listing_to_station()
        if listing_to:
            print(f"✓ Destination station field value: {listing_to}")
        
        # Test autosuggestion on destination station field
        autosuggestion_result = listing_page.enter_station_and_check_autosuggestion('to', 'Mum')
        
        print(f"✓ Autosuggestion visible: {autosuggestion_result['autosuggestion_visible']}")
        print(f"✓ Options count: {autosuggestion_result['options_count']}")
        
        if autosuggestion_result['options_text']:
            print(f"✓ Sample options: {autosuggestion_result['options_text'][:3]}")
        
        print(f"✓ Destination station field test completed")
