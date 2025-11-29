"""
Time manager - tracks game progression and quarters.
"""

import config


class TimeManager:
    """Manages game time and progression."""
    
    def __init__(self, total_quarters: int = None):
        self.total_quarters = total_quarters if total_quarters else config.GAME_DURATION_QUARTERS
        self.current_quarter = 0
        self.current_year = 1
        
    def advance_quarter(self) -> None:
        """Advance to the next quarter."""
        self.current_quarter += 1
        self.current_year = (self.current_quarter // 4) + 1
        
    def get_quarter_in_year(self) -> int:
        """Get the quarter within the current year (1-4)."""
        return (self.current_quarter % 4) + 1
        
    def is_year_end(self) -> bool:
        """Check if we're at the end of a fiscal year."""
        return self.get_quarter_in_year() == 4
        
    def is_game_over(self) -> bool:
        """Check if the game has ended."""
        return self.current_quarter >= self.total_quarters
        
    def quarters_remaining(self) -> int:
        """Get number of quarters remaining."""
        return max(0, self.total_quarters - self.current_quarter)
        
    def get_time_display(self) -> str:
        """Get formatted time display."""
        return f"Year {self.current_year}, Q{self.get_quarter_in_year()}"
        
    def get_progress_percentage(self) -> float:
        """Get game progress as percentage."""
        return (self.current_quarter / self.total_quarters) * 100
        
    def __str__(self) -> str:
        return self.get_time_display()

