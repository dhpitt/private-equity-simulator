"""
Private Equity Simulator - Main Entry Point

A terminal-based simulation game where you manage a private equity fund,
acquire companies, improve operations, and build portfolio value.
"""

from game.engine import GameEngine


def main():
    """Main entry point for the game."""
    try:
        engine = GameEngine()
        engine.start_game()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Thanks for playing!")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
