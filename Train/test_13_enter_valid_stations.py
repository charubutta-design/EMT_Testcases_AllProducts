"""
Test case for entering valid stations.
"""

import pytest
from pages.train_page import TrainPage


class TestEnterValidStations:
    """Test case for entering valid stations."""

    def test_enter_valid_stations(self, page):
        """
        Test entering valid source and destination stations.
        
        Verifies:
        - Stations can be entered successfully
        - Input values are captured correctly
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Enter valid stations
        from_city = "Delhi"
        to_city = "Mumbai"
        train_page.enter_stations(from_city, to_city)
        
        # Verify stations are entered
        from_value = train_page.get_from_station()
        to_value = train_page.get_to_station()
        
        assert from_city in from_value, f"From station should contain '{from_city}', got '{from_value}'"
        assert to_city in to_value, f"To station should contain '{to_city}', got '{to_value}'"
        print(f"✓ Valid stations entered: {from_value} → {to_value}")
