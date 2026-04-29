"""
Test case for swap stations interchanging values.
"""

import pytest
from pages.train_page import TrainPage


class TestSwapStationsInterchangesValues:
    """Test case for swap stations interchanging values."""

    def test_swap_stations_interchanges_values(self, page):
        """
        Test that clicking swap button interchanges from and to station values.
        
        Steps:
        1. Open the train booking page
        2. Enter "Delhi" as source and "Mumbai" as destination
        3. Capture station values before swap
        4. Click the swap button
        5. Capture station values after swap
        6. Assert that values are correctly interchanged
        
        Args:
            page: Playwright page fixture from conftest.py
        """
        # Initialize the TrainPage object with page fixture
        train_page = TrainPage(page)

        # Step 1: Navigate to the train booking page
        train_page.open_train_page()

        # Step 2: Enter source and destination stations
        from_city = "Delhi"
        to_city = "Mumbai"
        train_page.enter_stations(from_city, to_city)

        # Step 3: Capture the station values BEFORE swap
        from_station_before_swap = train_page.get_from_station()
        to_station_before_swap = train_page.get_to_station()

        # Log the values before swap (useful for debugging)
        print(f"\n--- Before Swap ---")
        print(f"From Station: {from_station_before_swap}")
        print(f"To Station: {to_station_before_swap}")

        # Step 4: Click the swap button to interchange stations
        train_page.click_swap()

        # Step 5: Capture the station values AFTER swap
        from_station_after_swap = train_page.get_from_station()
        to_station_after_swap = train_page.get_to_station()

        # Log the values after swap
        print(f"\n--- After Swap ---")
        print(f"From Station: {from_station_after_swap}")
        print(f"To Station: {to_station_after_swap}")

        # Step 6: Assert that the values are correctly interchanged
        # The original 'from' should now be in 'to' and vice versa
        assert from_station_after_swap == to_station_before_swap, (
            f"Expected From station to be '{to_station_before_swap}' "
            f"but got '{from_station_after_swap}'"
        )
        assert to_station_after_swap == from_station_before_swap, (
            f"Expected To station to be '{from_station_before_swap}' "
            f"but got '{to_station_after_swap}'"
        )

        print("\n✓ Swap functionality verified successfully!")
