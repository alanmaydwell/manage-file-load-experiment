# Manage File Load Experiment

Exploring a way of managing saving/uploading/migration of files in a way that allows them to be processed in successive chunks/batches.

Relies on two types of data files
- csv file with details of all the files to be processed.
- A text file that records progress, with the result of the most recent batch in its last line.


### Requirements
Works with Python v.3.14 and may work with some versions before this, although there's a type hint with a `|` character which breaks compatibility with some Python versions.

This only uses Python standard library - no additional dependencies.

### Using
Run `run_file_load.py` , e.g. `python3 run_file_load_.py` to run the load. It will "process" files listed in the file `file_details_example.csv` (although no actual file operations take place).

#### Basic Config

There are three key values at the top of the `main` function:

```
def main():
    # Could use env vars or command-line args to set these
    file_details_file = "file_details_example.csv"
    progress_file = "progress_log.txt"
    # Use 0 to indicate "unlimited"
    chunk_size = 0
```

- `file_details_file` - filename of CSV file with list of files to be read. The CSV file itself should have the filenames in its first column. Also no heading rows expected - data from the first row. The file `file_details_example.csv` is an example of this, and the file `utils/make_example_file.py` can be used to create this type of CSV file.
- `progress_file` - filename of the file used to log progress. This is not needed for the first run, which will create it.
- `chunk_size` - maximum number of files to process per run. Note a value of `0` represents "no limit", with all files processed in a single run. 

#### Tracking Progress
A file `progress_log.txt` is used to keep track of progress between each run. The last row in this file has the result of the most recent completed run. A run with chunk size `0` will produce a result like this:

```
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:31:03", "end_time": "2026-10-29_07:31:03", "first_row": 0, "last_row": 49, "status": "OK", "chunk_size": 0}
```

Repeated runs with chunk_size `3` will produce results like this:

```
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:34:44", "end_time": "2026-10-29_07:34:44", "first_row": 0, "last_row": 2, "status": "OK", "chunk_size": 3}
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:34:50", "end_time": "2026-10-29_07:34:50", "first_row": 3, "last_row": 5, "status": "OK", "chunk_size": 3}
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:34:51", "end_time": "2026-10-29_07:34:51", "first_row": 6, "last_row": 8, "status": "OK", "chunk_size": 3}
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:34:51", "end_time": "2026-10-29_07:34:51", "first_row": 9, "last_row": 11, "status": "OK", "chunk_size": 3}

```

#### Dealing with errors
A error during file operation stops the load. This can be simulated by including a filename in the CSV file that starts with `badfile`, which leads to result like the below:

```
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:38:11", "end_time": "2026-10-29_07:38:11", "first_row": 0, "last_row": 2, "status": "OK", "chunk_size": 3}
{"filename": "file_details_example.csv", "start_time": "2026-10-29_07:38:15", "end_time": "2026-10-29_07:38:15", "first_row": 3, "last_row": 4, "status": "The file 'badfile4.eg' is bad.", "chunk_size": 3}
```
The above shows a first chunk which was successful but the second chunk encountered an error. After an error, re-running `run_file_load_.py` will try to resume from the previosly failed row.