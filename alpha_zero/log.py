"""Log component for Deep RL Zoo."""
import collections
import os
import csv
from typing import List, Tuple


class CsvWriter:
    """A logging object writing to a CSV file.

    Each `write()` takes a `OrderedDict`, creating one column in the CSV file for
    each dictionary key on the first call. Successive calls to `write()` must
    contain the same dictionary keys.
    """

    def __init__(self, fname: str):
        """Initializes a `CsvWriter`.

        Args:
          fname: File name(path) for file to be written to.
        """
        if fname is not None and fname != '':
            dirname = os.path.dirname(fname)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

        self._fname = fname
        self._header_written = False
        self._fieldnames = None

    def write(self, values: collections.OrderedDict) -> None:
        """Appends given values as new row to CSV file."""
        if self._fname is None or self._fname == '':
            return

        if self._fieldnames is None:
            self._fieldnames = values.keys()

        # Check if already has rows
        if not self._header_written and os.path.exists(self._fname):
            with open(self._fname, 'r', encoding='utf8') as csv_file:
                content = csv.reader(csv_file)
                if len(list(content)) > 0:
                    self._header_written = True

        # Open a file in 'append' mode, so we can continue logging safely to the
        # same file after e.g. restarting from a checkpoint.
        with open(self._fname, 'a', encoding='utf8') as file_:
            # Always use same fieldnames to create writer, this way a consistency
            # check is performed automatically on each write.
            writer = csv.DictWriter(file_, fieldnames=self._fieldnames)

            # Write a header if this is the very first write.
            if not self._header_written:
                writer.writeheader()
                self._header_written = True
            writer.writerow(values)

    def close(self) -> None:
        """Closes the `CsvWriter`."""


def write_to_csv(writer: CsvWriter, log_output: List[Tuple]) -> None:
    writer.write(collections.OrderedDict((n, v) for n, v, _ in log_output))
