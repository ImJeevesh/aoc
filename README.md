# Advent of Code

Advent of Code - 2025

## Usage

The project includes a helper script `main.py` to manage and run solutions.

### Prerequisites

- Python

### Commands

**Create a new day structure:**
```bash
uv run main.py -c -d <day>
# Example: uv run main.py -c -d 1
# or
python main.py -c -d <day>
```
This will create a folder structure like `2025/1/` with solution and input files.

**Run a solution:**
```bash
python main.py -d <day>
# Example: python main.py -d 1
# or
uv run main.py -d <day>
```
By default, this runs `solution.py` against both `example.txt` and `input.txt`.

**Options:**

- `-y`, `--year`: Select year (default: current year)
- `-d`, `--day`: Select day (default: current day)
- `-c`, `--create`: Create day directory and templates
- `-e`, `--example`: Run only the example
- `-i`, `--input`: Run only the input

## Directory Structure

```
<year>/
  <day>/
    solution.py  # The solution code
    input.txt    # Puzzle input
    example.txt  # Example input
main.py          # Runner script
```
