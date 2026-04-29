"""
Test cases for multiple swap functionality.
"""

import pytest
from pages.train_page import TrainPage


class TestMultipleSwap:
    """Additional swap functionality tests."""

    def test_multiple_swap(self, page):
        """
        Test multiple consecutive swaps return to original state.
        
        Verifies:
        - Swap works correctly multiple times
        - Double swap returns to original state
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Enter stations
        train_page.enter_stations("Delhi", "Mumbai")
        
        # Capture original values
        original_from = train_page.get_from_station()
        original_to = train_page.get_to_station()
        
        # Perform first swap
        train_page.click_swap()
        
        # Verify first swap
        after_first_swap_from = train_page.get_from_station()
        after_first_swap_to = train_page.get_to_station()
        assert after_first_swap_from == original_to, "First swap failed for from station"
        assert after_first_swap_to == original_from, "First swap failed for to station"
        
        # Perform second swap (should return to original)
        train_page.click_swap()
        
        # Verify second swap returns to original
        final_from = train_page.get_from_station()
        final_to = train_page.get_to_station()
        assert final_from == original_from, "Double swap should return to original from station"
        assert final_to == original_to, "Double swap should return to original to station"
        
        print("✓ Multiple swap verified - double swap returns to original state")
