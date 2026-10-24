# Student Marks Report Generator

A beginner-friendly Python project that reads student marks from a CSV file, validates the input, calculates totals and percentages, assigns grades, and writes a processed report to a new CSV file.

## Features

- Reads CSV files using Python's built-in `csv` module.
- Checks that required columns and values are present.
- Rejects non-numeric marks and marks outside the range 0–100.
- Handles missing files, invalid data, and file access errors with useful messages.
- Calculates total marks, percentage, and grade.
- Creates the output directory when needed.
- Includes automated unit tests.

## Project structure

```text
student-marks-report/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── students.csv
├── output/
│   └── .gitkeep
└── tests/
    └── test_main.py
```

## Requirements

- Python 3.9 or newer
- No third-party packages are required. The program uses Python's standard library.
- `requirements.txt` is included for dependency documentation and standard project setup.

Check your Python version:

```bash
python --version
```

On some systems, use `python3 --version` instead.

## Setup and run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. (Optional but recommended) create a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install the listed requirements (there are currently no external dependencies):

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python main.py
   ```

The default input file is `data/students.csv`. The generated report is saved as `output/student_report.csv`.

### Use a different input or output file

You can provide file paths as command-line arguments:

```bash
python main.py data/students.csv output/student_report.csv
```

## CSV input format

The input CSV must contain these column names:

```csv
Name,Python,Database,Networking
Asha,92,88,95
Rahul,76,81,79
```

Each mark must be a whole number from 0 to 100. Blank rows are skipped. Missing required columns or invalid student records stop processing and display an error.

## Grade rules

| Percentage | Grade |
|---|---|
| 90–100 | A |
| 75–89.99 | B |
| 60–74.99 | C |
| 40–59.99 | D |
| Below 40 | F |

Percentage is the average across the three subjects.

## Example output

The output CSV contains the original marks plus `Total`, `Percentage`, and `Grade` columns. For example:

```csv
Name,Python,Database,Networking,Total,Percentage,Grade
Asha,92,88,95,275,91.67,A
```

## Run tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

The tests cover calculation, invalid marks, and report creation.

## Error handling

The program displays a helpful message when the input file is missing, required columns are absent, marks are invalid, no student records are available, or a file cannot be accessed. Correct the input CSV and run the program again.

## Limitations

- All three subject columns are required.
- Marks must be whole numbers; decimal marks are not accepted.
- The first invalid record stops processing so you can fix the source data before generating a report.

## License

This project is provided for learning and educational use. Add a license file if you choose a specific open-source license.
