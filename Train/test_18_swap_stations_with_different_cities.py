"""
Test case for swap stations with different cities.
"""

import pytest
from pages.train_page import TrainPage


class TestSwapStationsWithDifferentCities:
    """Test case for swap stations with different city combinations."""

    def test_swap_stations_with_different_cities(self, page):
        """
        Additional test with different city combinations.
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        # Initialize the TrainPage object
        train_page = TrainPage(page)

        # Open the train booking page
        train_page.open_train_page()

        # Test with different cities
        from_city = "Bangalore"
        to_city = "Chennai"
        train_page.enter_stations(from_city, to_city)

        # Capture values before swap
        from_before = train_page.get_from_station()
        to_before = train_page.get_to_station()

        # Perform swap
        train_page.click_swap()

        # Capture values after swap
        from_after = train_page.get_from_station()
        to_after = train_page.get_to_station()

        # Verify swap
        assert from_after == to_before, "From station not swapped correctly"
        assert to_after == from_before, "To station not swapped correctly"
        
        print("✓ Swap with different cities verified successfully!")
