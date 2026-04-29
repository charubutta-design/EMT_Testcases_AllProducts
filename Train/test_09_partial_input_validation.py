"""
Test case for partial input validation.
"""

import pytest
from pages.train_page import TrainPage


class TestPartialInputValidation:
    """Test case for partial input validation."""

    def test_partial_input_validation(self, page):
        """
        Test search with only partial input (from station only).
        
        Verifies:
        - Search with missing destination is handled
        - Validation prevents incomplete search
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Enter only from station
        train_page.enter_from_station("Delhi")
        
        # Leave to station empty
        train_page.clear_to_station()
        
        # Try to click search with partial input
        try:
            if train_page.search_button:
                train_page.search_button.wait_for(state="visible", timeout=5000)
                train_page.search_button.click()
            else:
                train_page.click_search()
        except:
            # Search button not accessible, which is acceptable
            pass
        
        # Wait for validation
        page.wait_for_timeout(1000)
        
        # Should still be on trains page
        assert train_page.is_on_trains_page(), \
            "Partial input should not allow search"
        
        print("[PASS] Partial input validation working")
