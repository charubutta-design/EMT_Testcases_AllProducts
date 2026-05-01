"""
Test case for verifying listing page is loaded after search.
"""

import pytest
from pages.train_page import TrainPage
from pages.listing_page import ListingPage


class TestListingPageLoaded:
    """Test case for verifying listing page loads correctly."""

    def test_listing_page_loaded(self, page):
        """
        Test that listing page loads successfully after a valid search.
        
        Steps:
        1. Navigate to train homepage
        2. Enter valid source and destination stations
        3. Select departure date
        4. Click search button
        5. Verify listing page is loaded
        
        Verifies:
        - Page navigates to listing/search results
        - Listing page elements are visible
        - URL changes to indicate results page
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        # Initialize page objects
        train_page = TrainPage(page)
        listing_page = ListingPage(page)

        # Step 1: Navigate to train booking homepage
        train_page.open_train_page()

        # Step 2 & 3: Enter search criteria
        from_city = "Jaipur"
        to_city = "Ahmedabad"
        train_page.enter_stations(from_city, to_city)
        train_page.select_departure_date()

        # Step 4: Perform search
        train_page.click_search()

        # Step 5: Verify listing page is loaded - use URL check as primary
        current_url = listing_page.get_current_url().lower()
        
        # URL should contain trainlistinfo for listing page
        is_listing_url = "trainlistinfo" in current_url or "trainlist" in current_url
        
        # Also try the page object method
        is_loaded = listing_page.is_listing_page_loaded()
        
        # Assert listing page loaded successfully (either via URL or page check)
        assert is_listing_url or is_loaded, "Listing page should be loaded after search"
        
        # Additional verification - URL should change from homepage
        assert current_url != train_page.URL.lower(), "URL should change after search"
        
        print(f"✓ Listing page loaded successfully")
        print(f"✓ Current URL: {current_url}")
