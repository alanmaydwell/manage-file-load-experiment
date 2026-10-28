def migrate_file(filename: str) -> list[str]:
    """
    Placeholder for saving file - doesn't actually save anything
    but does return error message if filename starts "badfile"
    """
    errors = []
    if filename.startswith("badfile"):
        errors.append(f"The file '{filename}' is bad.")
    print("Dummy file process:", filename, "errors:", errors)
    return errors


def process_csv_row(row: str) -> list[str]:
    errors = []
    items = [e.strip() for e in row.split(",")]
    if items:
        filename = items[0]
        file_errors = migrate_file(filename)
        if file_errors:
            errors.extend(file_errors)
    else:
        errors.append("No details from csv row")
    return errors


def process_csv_file(filename: str,
                     start_row: int = 0,
                     chunk_size: int = 0) -> tuple[int, int, list[str]]:
    # Subtracting 1 because first row is row 0, so when chunk_size is 1 we want
    # to stop before 2nd row, which is row 1
    row_limit = start_row + chunk_size - 1
    row_limit_active: bool = chunk_size != 0
    result = []
    try:
        with open(filename, "r") as infile:
            for ri, row in enumerate(infile):
                # There likely is a more efficient way of reaching start_row,
                # e.g. using seek, but this would be at expense of readability
                if ri >= start_row:
                    errors = process_csv_row(row)
                    if errors:
                        print(f"Ending as error encountered - row: {ri}, errors: {errors}")
                        break
                # End if row limit set and reached. Note file at the limit will
                # still have been processed in the step above.
                if row_limit_active and ri >= row_limit:
                    print(f"Ending as row-limit reached - last file from row: {ri}")
                    break
    except FileNotFoundError:
        ri = start_row
        result.append(f"Migration file '{filename}' not found")
    return start_row, ri, errors
