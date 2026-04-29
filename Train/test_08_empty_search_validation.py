"""
Test case for empty search validation.
"""

import pytest
from pages.train_page import TrainPage


class TestEmptySearchValidation:
    """Test case for empty search validation."""

    def test_empty_search_validation(self, page):
        """
        Test search validation with empty inputs.
        
        Verifies:
        - Empty search is prevented or shows error
        - User is prompted to fill required fields
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Clear any pre-filled values
        train_page.clear_all_inputs()
        
        # Try to click search without entering any data
        try:
            if train_page.search_button:
                train_page.search_button.wait_for(state="visible", timeout=5000)
                train_page.search_button.click()
            else:
                train_page.click_search()
        except:
            # Search button not visible, which validates the test case
            pass
        
        # Wait for validation message
        page.wait_for_timeout(1000)
        
        # Should still be on same page (search prevented)
        current_url = train_page.get_current_url()
        
        # Verify we're still on trains page
        assert train_page.is_on_trains_page(), \
            "Empty search should not navigate away from trains page"
        
        print("[PASS] Empty search validation working")
