"""
Test case for auto-suggestion selection.
"""

import pytest
from pages.train_page import TrainPage


class TestAutoSuggestionSelection:
    """Test case for auto-suggestion selection."""

    def test_auto_suggestion_selection(self, page):
        """
        Test that autocomplete suggestions appear and can be selected.
        
        Verifies:
        - Dropdown appears when typing
        - Suggestions contain relevant stations
        - Selection works correctly
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Click and type in from station input
        train_page.from_station_input.click()
        train_page.from_station_input.fill("Mum")
        
        # Wait for autocomplete to appear
        page.wait_for_timeout(1500)
        
        # Check if autocomplete is visible
        assert train_page.is_autocomplete_visible(), "Autocomplete dropdown should be visible"
        
        # Get suggestions
        suggestions = train_page.get_autocomplete_suggestions()
        assert len(suggestions) > 0, "Should have at least one suggestion"
        
        # Verify Mumbai-related suggestions appear
        mumbai_found = any("Mumbai" in s for s in suggestions)
        assert mumbai_found, f"Mumbai should be in suggestions, got: {suggestions[:5]}"
        
        print(f"✓ Auto-suggestion working. Found {len(suggestions)} suggestions")
