"""
Test case for past date validation.
"""

import pytest
from datetime import datetime, timedelta
from pages.train_page import TrainPage


class TestPastDateNotSelectable:
    """Test case for past date validation."""

    def test_past_date_not_selectable(self, page):
        """
        Test that past dates cannot be selected.
        
        Verifies:
        - Past dates are disabled in date picker
        - System prevents past date selection
        """
        train_page = TrainPage(page)
        train_page.open_train_page()
        
        # Calculate a past date
        past_date = (datetime.now() - timedelta(days=7)).strftime('%d/%m/%Y')
        
        # Check if past date is selectable
        is_selectable = train_page.is_date_selectable(past_date)
        
        assert not is_selectable, f"Past date {past_date} should not be selectable"
        print(f"✓ Past date validation working - {past_date} not selectable")
