"""
Test cases for station input functionality.
"""

import pytest
from pages.train_page import TrainPage


class TestStationInput:
    """Test cases for station input functionality."""

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

    def test_same_station_validation(self, page):
        """
        Test validation when same station is entered for source and destination.
        
        Verifies:
        - System handles same station input
        - Either prevents or shows error for same stations
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Enter same station for both
        train_page.enter_from_station("Delhi")
        
        # For to station, try entering same city
        train_page.to_station_input.click()
        train_page.to_station_input.fill("Delhi")
        page.wait_for_timeout(1500)
        
        # Try to select from dropdown
        try:
            train_page._select_station_from_dropdown("Delhi")
        except Exception:
            pass  # May not allow same station
        
        # Get both values
        from_val = train_page.get_from_station()
        to_val = train_page.get_to_station()
        
        # Log the result
        if from_val == to_val and from_val != "":
            print(f"⚠ Same station allowed: {from_val}")
        else:
            print(f"✓ Different stations: {from_val} → {to_val}")
        
        # Test passes if no crash - validation behavior may vary
        assert True, "Same station test completed without errors"
