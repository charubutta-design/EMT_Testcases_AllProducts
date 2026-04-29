"""
Test case for invalid station input handling.
"""

import pytest
from pages.train_page import TrainPage


class TestInvalidStationInput:
    """Test case for invalid station input handling."""

    def test_invalid_station_input(self, page):
        """
        Test behavior with invalid/non-existent station names.
        
        Verifies:
        - Invalid input doesn't cause errors
        - No suggestions appear for gibberish input
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Enter invalid station name
        train_page.from_station_input.click()
        train_page.from_station_input.fill("XYZABC123")
        
        # Wait for potential autocomplete
        page.wait_for_timeout(2000)
        
        # Either no suggestions or autocomplete not visible
        suggestions = train_page.get_autocomplete_suggestions()
        
        # Invalid input should have no relevant suggestions
        assert len(suggestions) == 0 or not train_page.is_autocomplete_visible(), \
            "Invalid station should have no suggestions"
        
        print("✓ Invalid station input handled correctly")
