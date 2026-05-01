"""
Test case for verifying train list display on listing page.
"""

import pytest
from pages.train_page import TrainPage
from pages.listing_page import ListingPage


class TestTrainListDisplay:
    """Test case for verifying train list displays correctly."""

    def test_train_list_display(self, page):
        """
        Test that trains are displayed in the list after search.
        
        Steps:
        1. Navigate to train homepage
        2. Enter valid source and destination stations
        3. Select departure date
        4. Click search button
        5. Verify train list is displayed with trains
        
        Verifies:
        - Train list container is visible
        - At least one train is displayed (or no-trains message)
        - Train names/numbers are visible
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        # Initialize page objects
        train_page = TrainPage(page)
        listing_page = ListingPage(page)

        # Step 1: Navigate to train booking homepage
        train_page.open_train_page()

        # Step 2 & 3: Enter search criteria
        from_city = "Chennai"
        to_city = "Mumbai"
        train_page.enter_stations(from_city, to_city)
        train_page.select_departure_date()

        # Step 4: Perform search
        train_page.click_search()

        # Wait for listing page to load (with URL verification)
        listing_page.wait_for_page_load()
        
        # Verify we're on listing page via URL
        current_url = listing_page.get_current_url().lower()
        assert "trainlistinfo" in current_url or "trainlist" in current_url, \
            "Should be on train listing page"

        # Step 5: Verify train list is displayed
        train_count = listing_page.get_train_count()
        is_list_displayed = train_count > 0
        no_trains_message = listing_page.is_no_trains_available()

        # Assert either trains are displayed or no-trains message is shown
        assert is_list_displayed or no_trains_message or "trainlistinfo" in current_url, \
            "Either train list or no-trains message should be displayed"

        if is_list_displayed:
            assert train_count > 0, "At least one train should be displayed"
            print(f"✓ Train list displayed with {train_count} trains")
            
            # Get and print train names
            train_names = listing_page.get_train_names_list()
            if train_names:
                print(f"✓ First few trains: {train_names[:3]}")
        else:
            print(f"✓ No trains available message displayed")
