import time
from modules.track_progress import MigrationState, get_resumption_row, save_latest_state
from modules.manage_files import process_csv_file


def nowstr() -> str:
    return time.strftime("%Y-%m-%d_%H:%M:%S")


def main():
    # Could use env vars or command-line args to set these
    file_details_file = "file_details_example.csv"
    progress_file = "progress_log.txt"
    # Use 0 to indicate "unlimited"
    chunk_size = 3

    # Work out where to resume the load, based on previous state if it exists
    start_row = get_resumption_row(progress_file)

    # Process CSV file with range based on start_row and chunk_size
    start_time = nowstr()
    first_row, last_row, errors = process_csv_file(file_details_file, start_row, chunk_size)
    end_time = nowstr()

    # Record outcome of the load

    # A bit clunky - as we're reading the CSV file line-by-line, it's hard
    # to tell early if first_row beyond end of file
    if first_row > last_row:
        final_state = f"OK - first row {first_row} likely beyond the end of file - no rows processed"
    elif not errors:
        final_state = "OK"
    else:
        final_state = ", ".join(errors)
    details = MigrationState(file_details_file, start_time, end_time, first_row, last_row, final_state, chunk_size)
    save_latest_state(progress_file, details)
    print(f"Run end: {details}")

if __name__ == "__main__":
    main()
