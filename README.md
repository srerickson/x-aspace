# ArchivesSpace API Exploration

These scripts use [ArchivesSnake](https://github.com/archivesspace-labs/ArchivesSnake) to interact with the ArchivesSpace API. 

## Requirements

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) for dependency management
- Ability to connect to an ArchivesSpace instance

## Setup

1. **Configure ArchivesSnake**
   Create `.archivessnake.yml` in your home directory with your ArchivesSpace credentials:
   ```yaml
   baseurl: http://your-archives-space-url:8089
   username: admin
   password: admin
   ```
   See the [ArchivesSnake documentation](https://github.com/archivesspace-labs/ArchivesSnake?tab=readme-ov-file#configuration) for more configuration options.

2. **Set up the development environment**
   ```bash
   # Install uv if you haven't already
   pip install uv

   # Create and activate a virtual environment
   uv venv

   # Activate the virtual environment
   # On Unix/macOS:
   source .venv/bin/activate
   # On Windows:
   .venv\Scripts\activate

   # Install dependencies
   uv pip install -r pyproject.toml
   ```

## Available Scripts

### `fix_dates.py`

This script fixes date types in ArchivesSpace records where inclusive dates have identical begin/end dates, converting them to single dates.

Usage:

```bash
$ uv run fix_dates.py --repo-id 2 --resource-id 1463
```