"""
Input handlers - standardized user input methods.
"""

from typing import List, Optional, Any


def prompt_choice(options: List[str], prompt: str = "Select an option") -> int:
    """
    Prompt user to select from a list of options.
    
    Args:
        options: List of option strings
        prompt: Prompt message
        
    Returns:
        Index of selected option (0-based)
    """
    print(f"\n{prompt}:")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
        
    while True:
        try:
            choice = input("\nEnter your choice: ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(options):
                return choice_num - 1
            else:
                print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            return -1


def prompt_number(
    prompt: str = "Enter a number",
    min_value: float = None,
    max_value: float = None,
    allow_float: bool = True
) -> Optional[float]:
    """
    Prompt user for a numeric input.
    
    Args:
        prompt: Prompt message
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        allow_float: Whether to allow decimal numbers
        
    Returns:
        Number entered by user, or None if cancelled
    """
    range_str = ""
    if min_value is not None and max_value is not None:
        range_str = f" ({min_value:,.0f} - {max_value:,.0f})"
    elif min_value is not None:
        range_str = f" (min: {min_value:,.0f})"
    elif max_value is not None:
        range_str = f" (max: {max_value:,.0f})"
        
    while True:
        try:
            value_str = input(f"\n{prompt}{range_str}: ").strip()
            
            if not value_str:
                return None
                
            if allow_float:
                value = float(value_str)
            else:
                value = int(value_str)
                
            if min_value is not None and value < min_value:
                print(f"Value must be at least {min_value:,.0f}")
                continue
                
            if max_value is not None and value > max_value:
                print(f"Value must be at most {max_value:,.0f}")
                continue
                
            return value
            
        except ValueError:
            print("Please enter a valid number")
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled")
            return None


def prompt_yes_no(prompt: str = "Continue?", default: bool = True) -> bool:
    """
    Prompt user for yes/no input.
    
    Args:
        prompt: Prompt message
        default: Default value if user just presses Enter
        
    Returns:
        True for yes, False for no
    """
    default_str = "Y/n" if default else "y/N"
    
    while True:
        try:
            response = input(f"\n{prompt} [{default_str}]: ").strip().lower()
            
            if not response:
                return default
                
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
                
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled")
            return False


def prompt_text(prompt: str = "Enter text", allow_empty: bool = False) -> Optional[str]:
    """
    Prompt user for text input.
    
    Args:
        prompt: Prompt message
        allow_empty: Whether to allow empty strings
        
    Returns:
        Text entered by user, or None if cancelled
    """
    while True:
        try:
            text = input(f"\n{prompt}: ").strip()
            
            if not text and not allow_empty:
                print("Please enter some text")
                continue
                
            return text
            
        except (KeyboardInterrupt, EOFError):
            print("\nCancelled")
            return None


def press_enter_to_continue(message: str = "Press Enter to continue...") -> None:
    """Wait for user to press Enter."""
    try:
        input(f"\n{message}")
    except (KeyboardInterrupt, EOFError):
        pass


def clear_screen() -> None:
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

