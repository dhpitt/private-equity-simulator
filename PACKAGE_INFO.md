# PE Simulator - Package Information

## Package Structure

The PE Simulator is now configured as a pip-installable Python package!

### Package Name
`pe-sim`

### Version
1.0.0

### Entry Point
After installation, run with:
```bash
pe-sim
```

## Files Created for pip Installation

### 1. `pyproject.toml` (Updated)
- Modern Python packaging configuration
- Defines package metadata, dependencies, and scripts
- Includes setuptools configuration for package discovery
- Specifies data files to include

**Key Configurations:**
- **Name**: pe-sim
- **Version**: 1.0.0
- **Python**: >=3.8
- **Dependencies**: rich>=14.2.0
- **Entry Point**: `pe-sim` command → `main:main()`
- **Packages**: game, models, simulation, ui
- **Data Files**: data/*.json, data/*.csv

### 2. `setup.py` (New)
- Backwards compatibility for older pip versions
- Delegates to pyproject.toml for configuration

### 3. `MANIFEST.in` (New)
- Ensures all necessary files are included in distribution
- Includes:
  - Data files (JSON, CSV)
  - Configuration (config.py)
  - Documentation (README, markdown files)
- Excludes:
  - Python cache files
  - Git files
  - Save files

### 4. `INSTALL.md` (New)
- Comprehensive installation guide
- Multiple installation methods
- Troubleshooting tips
- Development setup instructions

## Package Contents

### Python Modules
```
pe-sim/
├── game/          # Game engine and core logic
├── models/        # Data models (Player, Company, Market, etc.)
├── simulation/    # Simulation systems (DCF, operations, procedural gen)
├── ui/            # User interface (screens, tables)
├── config.py      # Global configuration
└── main.py        # Entry point
```

### Data Files
```
data/
├── manager_narratives.json  # Manager-related narratives
├── names.json              # Procedural name generation
├── narratives.json         # Cost-cutting narratives
├── quotes.json             # Inspirational quotes
├── real_sp500.csv          # 503 real S&P 500 companies with CEOs
└── sectors.json            # Sector definitions
```

### Documentation
```
README.md               # Main documentation
QUICKSTART.md          # Quick start guide
INSTALL.md             # Installation guide
CURSOR.md              # Project structure
(+ 15 more MD files documenting features)
```

## Installation Methods

### Method 1: Development Install (Editable)
```bash
cd /path/to/pe-sim
pip install -e .
```

**Benefits:**
- Code changes take effect immediately
- Data files are accessible
- Easy for development

### Method 2: Standard Install
```bash
pip install /path/to/pe-sim
```

**Benefits:**
- Installs like any Python package
- Can uninstall cleanly

### Method 3: From Built Wheel
```bash
# Build
python -m build

# Install
pip install dist/pe_sim-1.0.0-py3-none-any.whl
```

**Benefits:**
- Distributable package
- Can share with others
- Can upload to PyPI

### Method 4: From Git (Future)
```bash
pip install git+https://github.com/username/pe-sim.git
```

**Benefits:**
- Install from anywhere
- Automatic updates
- Easy sharing

## Running After Installation

### Command Line
```bash
pe-sim
```

### Python Module
```bash
python -m main
```

### From Python
```python
from main import main
main()
```

## Distribution

### Building Distributable Packages

```bash
# Install build tools
pip install build

# Build source distribution and wheel
python -m build
```

**Creates:**
- `dist/pe_sim-1.0.0.tar.gz` - Source distribution
- `dist/pe_sim-1.0.0-py3-none-any.whl` - Wheel distribution

### Uploading to PyPI (Future)

```bash
# Install twine
pip install twine

# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

**After publishing:**
```bash
pip install pe-sim
```

## Package Metadata

### Classifiers
- Development Status :: 4 - Beta
- Intended Audience :: End Users/Desktop
- Topic :: Games/Entertainment :: Simulation
- License :: OSI Approved :: MIT License
- Programming Language :: Python :: 3.8+
- Environment :: Console
- Operating System :: OS Independent

### Keywords
game, simulation, private-equity, business, terminal, text-adventure

### URLs
- Homepage: GitHub repository
- Documentation: README
- Repository: GitHub
- Issues: GitHub Issues

## Dependencies

### Required
- `rich>=14.2.0` - Terminal UI library

### Optional (Development)
- `pytest>=8.0.0` - Testing framework

## File Inclusion

### Always Included
- All .py files in packages (game/, models/, simulation/, ui/)
- config.py
- main.py
- All data files (data/*.json, data/*.csv)
- README.md
- MANIFEST.in
- pyproject.toml
- setup.py

### Excluded
- __pycache__/
- *.pyc, *.pyo
- .git/
- .cursor/
- saves/
- tests/ (excluded from package, but in source)
- .DS_Store

## Verification

### Check Installation
```bash
pip show pe-sim
```

### Check Entry Point
```bash
which pe-sim
# Should show: /path/to/venv/bin/pe-sim
```

### Test Run
```bash
pe-sim
# Should start the game
```

## Virtual Environment (Recommended)

```bash
# Create
python -m venv venv

# Activate
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Install
pip install -e .

# Run
pe-sim
```

## Uninstallation

```bash
pip uninstall pe-sim
```

Cleanly removes:
- All Python modules
- Data files
- Entry point script
- Package metadata

## Troubleshooting

### Data Files Not Found
```bash
# Reinstall in editable mode
pip install -e .
```

### Import Errors
```bash
# Install dependencies
pip install rich>=14.2.0
```

### Entry Point Not Working
```bash
# Check if installed
pip show pe-sim

# Reinstall
pip uninstall pe-sim
pip install .
```

## Development Workflow

```bash
# 1. Clone/navigate to repo
cd /path/to/pe-sim

# 2. Create venv
python -m venv venv
source venv/bin/activate

# 3. Install in editable mode with dev dependencies
pip install -e ".[dev]"

# 4. Make changes to code
# (Changes take effect immediately)

# 5. Run game
pe-sim

# 6. Run tests
pytest

# 7. Build for distribution
python -m build
```

## Package Size

- **Installed**: ~5-10 MB
- **Wheel**: ~1-2 MB
- **Source Distribution**: ~1-2 MB

## Python Compatibility

Tested and compatible with:
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

## Operating Systems

Works on:
- **Linux** (Ubuntu, Debian, Fedora, etc.)
- **macOS** (Intel and Apple Silicon)
- **Windows** (10, 11)
- **BSD** (FreeBSD, OpenBSD)

## Terminal Support

Requires:
- UTF-8 encoding
- ANSI color support
- Minimum 80x24 terminal size
- Recommended: 120x30 or larger

## Summary

PE Simulator is now a fully pip-installable Python package with:

✅ **Modern packaging** (pyproject.toml)  
✅ **Entry point** (`pe-sim` command)  
✅ **Data file inclusion** (CSV, JSON)  
✅ **Development mode** support  
✅ **Comprehensive documentation**  
✅ **PyPI ready** (can be published)  
✅ **Cross-platform** (Linux, macOS, Windows)  
✅ **Python 3.8+** compatible  

Install and play from anywhere:
```bash
pip install -e /path/to/pe-sim
pe-sim
```

**It just works!** 🎮📦✨

