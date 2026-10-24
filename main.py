"""Validate student marks from CSV and generate a summary report."""
import csv
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "data" / "students.csv"
DEFAULT_OUTPUT = BASE_DIR / "output" / "student_report.csv"
SUBJECTS = ("Python", "Database", "Networking")
MAX_MARK = 100


class DataValidationError(ValueError):
    """Raised when a student record contains invalid data."""


def validate_record(row, line_number):
    """Validate and normalize one CSV record."""
    name = (row.get("Name") or "").strip()
    if not name:
        raise DataValidationError(f"Line {line_number}: student name is missing.")

    marks = []
    for subject in SUBJECTS:
        raw = (row.get(subject) or "").strip()
        if not raw:
            raise DataValidationError(
                f"Line {line_number}: {subject} mark is missing for {name}."
            )
        try:
            mark = int(raw)
        except ValueError as exc:
            raise DataValidationError(
                f"Line {line_number}: {subject} mark for {name} must be a whole number."
            ) from exc
        if not 0 <= mark <= MAX_MARK:
            raise DataValidationError(
                f"Line {line_number}: {subject} mark for {name} must be between 0 and 100."
            )
        marks.append(mark)

    total = sum(marks)
    percentage = total / len(SUBJECTS)
    if percentage >= 90:
        grade = "A"
    elif percentage >= 75:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 40:
        grade = "D"
    else:
        grade = "F"

    return {
        "Name": name,
        "Python": marks[0],
        "Database": marks[1],
        "Networking": marks[2],
        "Total": total,
        "Percentage": f"{percentage:.2f}",
        "Grade": grade,
    }


def process_csv(input_path=DEFAULT_INPUT, output_path=DEFAULT_OUTPUT):
    """Read, validate, and process CSV records; return the number processed."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(f"Input CSV file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed = []
    expected_headers = {"Name", *SUBJECTS}

    with input_path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise DataValidationError("The input CSV is empty or has no header row.")
        missing = expected_headers - set(reader.fieldnames)
        if missing:
            raise DataValidationError(
                "Missing required CSV column(s): " + ", ".join(sorted(missing))
            )

        for line_number, row in enumerate(reader, start=2):
            if not row or all(not (value or "").strip() for value in row.values()):
                continue
            processed.append(validate_record(row, line_number))

    if not processed:
        raise DataValidationError("No valid student records were found in the input CSV.")

    fieldnames = ["Name", *SUBJECTS, "Total", "Percentage", "Grade"]
    with output_path.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed)

    return len(processed)


def main():
    """Run the application, optionally accepting input and output paths."""
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT
    try:
        count = process_csv(input_path, output_path)
    except (FileNotFoundError, PermissionError, DataValidationError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except csv.Error as exc:
        print(f"Error: Could not read or write CSV data: {exc}", file=sys.stderr)
        return 1

    print(f"Success! Processed {count} student record(s).")
    print(f"Report saved to: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
