# Installation Guide - PE Simulator

## Installing from Source

### Prerequisites
- Python 3.8 or higher
- uv package manager (recommended) or pip

### Installation Methods

#### Method 1: Install in Development Mode (Recommended for Development)

This allows you to edit the code and see changes immediately:

```bash
# Clone or navigate to the pe-sim directory
cd /path/to/pe-sim

# Activate virtual environment (if using one)
source .venv/bin/activate

# Install in editable/development mode
uv pip install -e .

# Or with development dependencies
uv pip install -e ".[dev]"
```

**Using regular pip:**
```bash
pip install -e .
pip install -e ".[dev]"
```

#### Method 2: Install as a Package

This installs it like any other Python package:

```bash
# From the pe-sim directory
uv pip install .

# Or directly from a specific path
uv pip install /path/to/pe-sim
```

**Using regular pip:**
```bash
pip install .
```

#### Method 3: Install from a Wheel

Build and install from a wheel:

```bash
# Build the package
python -m pip install build
python -m build

# Install the wheel
pip install dist/pe_sim-1.0.0-py3-none-any.whl
```

#### Method 4: Install from Git (if hosted)

```bash
# Install directly from GitHub (when available)
pip install git+https://github.com/yourusername/pe-sim.git

# Or a specific branch/tag
pip install git+https://github.com/yourusername/pe-sim.git@main
```

## Running the Game

After installation, you can run the game from anywhere:

```bash
pe-sim
```

Or using Python module syntax:

```bash
python -m main
```

## Verifying Installation

Check if the package is installed:

```bash
uv pip show pe-sim
```

Or with regular pip:
```bash
pip show pe-sim
```

You should see output like:

```
Name: pe-sim
Version: 1.0.0
Summary: Private Equity Simulator - A terminal-based business simulation game
Location: /path/to/site-packages
Requires: rich
```

## Uninstalling

```bash
uv pip uninstall pe-sim
```

Or with regular pip:
```bash
pip uninstall pe-sim
```

## Troubleshooting

### Data Files Not Found

If you get errors about missing data files (JSON, CSV), ensure you installed with:

```bash
pip install -e .  # Development mode includes all files
```

Or reinstall:

```bash
pip uninstall pe-sim
pip install .
```

### Import Errors

If you get import errors, make sure all dependencies are installed:

```bash
pip install rich>=14.2.0
```

### Python Version Issues

PE Simulator requires Python 3.8+. Check your version:

```bash
python --version
```

If you have multiple Python versions:

```bash
python3 --version
python3.8 --version
python3.11 --version
```

Use the appropriate pip version:

```bash
python3.11 -m pip install -e .
```

## Development Setup

For development with testing:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Or with coverage
pytest --cov=.
```

## Building for Distribution

To create distributable packages:

```bash
# Install build tools
pip install build twine

# Build source distribution and wheel
python -m build

# This creates:
#   dist/pe_sim-1.0.0.tar.gz       (source distribution)
#   dist/pe_sim-1.0.0-py3-none-any.whl  (wheel)
```

## Publishing to PyPI (For Maintainers)

```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Then real PyPI
twine upload dist/*
```

After publishing, users can install with:

```bash
pip install pe-sim
```

## Directory Structure After Installation

When installed, the package structure is:

```
site-packages/
├── pe_sim-1.0.0.dist-info/
├── game/
├── models/
├── simulation/
├── ui/
├── config.py
├── main.py
└── data/
    ├── manager_narratives.json
    ├── names.json
    ├── narratives.json
    ├── quotes.json
    ├── real_sp500.csv
    └── sectors.json
```

## Virtual Environment (Recommended)

Always use a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install
pip install -e .

# Run
pe-sim

# Deactivate when done
deactivate
```

## Quick Start After Installation

```bash
# Install
pip install -e .

# Run the game
pe-sim

# Select difficulty (Obama Era / Reagan Era / Newsom Era)
# Choose your fund name
# Start acquiring companies!
```

## System Requirements

- **OS**: Linux, macOS, Windows
- **Python**: 3.8+
- **Terminal**: Any modern terminal with UTF-8 support
- **Disk Space**: ~10 MB
- **RAM**: Minimal (<50 MB during gameplay)

## Optional: Shell Alias

Add an alias to your shell config (~/.bashrc, ~/.zshrc):

```bash
alias pes='pe-sim'
```

Then run with just:

```bash
pes
```

## Support

For issues or questions:
1. Check this installation guide
2. Review the README.md
3. Check existing issues on GitHub
4. Create a new issue with details about your system and error messages

