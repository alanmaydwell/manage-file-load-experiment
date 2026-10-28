import os


def make_file(filename: str, rows: int):
    with open(filename, "w") as outfile:
        for i in range(rows):
            outfile.write(f"file{i}.eg, {i}, {os.urandom(32).hex()}\n")


if __name__ == "__main__":
    filename = "file_details_example.csv"
    rows = 50
    make_file(filename, rows)
    print(f"Created {filename} with {rows} rows")
