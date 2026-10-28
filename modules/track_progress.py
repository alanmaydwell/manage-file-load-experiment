from dataclasses import dataclass, asdict
import json


@dataclass
class MigrationState:
    filename: str
    start_time: str
    end_time: str
    first_row: int
    last_row: int
    status: str
    # Zero chunk_size means "unlimited"
    chunk_size: int = 0


def get_latest_state(status_filename: str) -> MigrationState | None:
    try:
        with open(status_filename, "r") as status_file:
            # Not efficient for big file but this one should be small
            lines = status_file.readlines()
            if lines:
                details = lines[-1]
    # Missing file can be fine as status file not expected on first run
    except FileNotFoundError:
        details = None
        print(f"Status file {status_filename} not found on start. Will be created")

    if details:
        details_dict = json.loads(details)
        migration_state = MigrationState(**details_dict)
    else:
        migration_state = None

    return migration_state


def save_latest_state(status_filename: str, details: MigrationState):
    line = json.dumps(asdict(details))
    with open(status_filename, "a") as status_file:
        status_file.write(line + "\n")


def get_resumption_row(status_filename: str,
                       skip_previous_failure: bool = False) -> int:
    start_row = 0
    previous_state = get_latest_state(status_filename)
    if previous_state:
        # Advance to next row if previous run ended without error, otherwise
        # resume from the failed row unless skip_previous_failure set
        if previous_state.status.startswith("OK") or skip_previous_failure:
            start_row = previous_state.last_row + 1
        else:
            start_row = previous_state.last_row
    return start_row
