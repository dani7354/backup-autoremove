#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from time import strptime
import os
import re
import sys
import shutil
import traceback


def _parse_args() -> Namespace:
    parser = ArgumentParser(description="Deletes the oldest backups (files or folders) at the specified location",
                            add_help=False)
    parser.add_argument("-l", "--location", dest="location", type=str, required=True,
                        help="Folder containing the backup folders or files")
    parser.add_argument("-d", "--date-format", dest="date_format", type=str, required=True,
                        help="Format for parsing the date from the file or folder name (e.g. %Y-%m-%d)")
    parser.add_argument("-p", "--regex-pattern", dest="regex_pattern", type=str, required=True,
                        help="Regex pattern that matches the date in file or folder name")
    parser.add_argument("-m", "--max-backup-count", dest="max_backups", type=int, required=True,
                        help="Number of backups allowed at the specified location")
    parser.add_argument("-fp", "--file-pattern", dest="file_pattern", type=str, required=False,
                        help="File pattern to filter the files or folders at the location")

    return parser.parse_args()


def _list_files(location_path: str, file_pattern: str) -> list[str]:
    return [
        os.path.join(location_path, file_name) for file_name in os.listdir(location_path)
        if re.match(file_pattern, file_name)
    ]


def parse_date(regex_pattern: str, filename: str, date_format: str):
    if regex_pattern is None or len(regex_pattern) < 1:
        raise ValueError("Argument 'regex_pattern' cannot be None or empty!")
    if filename is None or len(filename) < 1:
        raise ValueError("Argument 'filename' cannot be None or empty!")

    regex_match = re.search(regex_pattern, filename)
    if not regex_match is None:
        if not date_format is None:
            date_time = strptime(regex_match.group(), date_format)
        else:
            date_time = strptime(regex_match.group())

        return date_time
    return False


def get_backups_to_remove(all_backups, max_backup_count):
    if max_backup_count < 0:
        raise ValueError("Argument 'max_backup_count' cannot be less than 0")

    backups_to_remove = []
    remove_count = len(all_backups) - max_backup_count if not all_backups is None else 0
    if remove_count > 0:
        all_backups.sort(key=lambda e: e[0])
        for i in range(0, remove_count):
            backups_to_remove.append(all_backups[i][1])
    return backups_to_remove


def location_is_valid(path) -> bool:
    return path and os.path.isdir(path) and os.access(path, os.R_OK | os.W_OK)

def main() -> None:
    try: pass
    except Exception as ex:
        print(f"An exception was thrown: {ex}\nStackTrace: {traceback.format_exc()}")

if __name__ == "__main__":
    try:
        print(f"Runnning {sys.argv[0]}...")
        arguments = _parse_args()

        location = arguments.location
        date_regex_pattern = arguments.regex_pattern
        date_format = arguments.date_format
        max_backups = arguments.max_backups

        if not location_is_valid(arguments.location):
            raise ValueError(
                "Invalid value for argument for '-l, --location'. "
                "Check if the folder exists and the user has RW permissions!")

        print(f"Reading files at {location}")
        files = os.listdir(location)
        backups = []
        for file in files:
            try:
                backup_datetime = parse_date(arguments["regex_pattern"], file, arguments["date_format"])
                if backup_datetime is False:
                    continue
                print(f"Backup found: {file}")
                backups.append((backup_datetime, file))
            except ValueError:
                print(f"Error parsing date from file: {file} - skipping to next!")
                continue

        print("Checking for backups to remove...")
        backups_to_remove = get_backups_to_remove(backups, arguments["max_backups"])
        print(f"{len(backups_to_remove)} backups will be removed!")
        for backup in backups_to_remove:
            backup_path = os.path.join(arguments["location"], backup)
            if os.path.exists(os.path.join(arguments["location"], backup)):
                print(f"Removing {backup_path}...")
                if os.path.isdir(backup_path):
                    shutil.rmtree(backup_path)
                elif os.path.isfile(backup_path):
                    os.remove(backup_path)

    except ValueError as error:
        print(f"A ValueError was thrown: {error}\nStackTrace: {traceback.format_exc()}")
        sys.exit(1)
    except OSError as error:
        print(f"An OSError was thrown: {error}\nStackTrace: {traceback.format_exc()}")
        sys.exit(1)
    except Exception as error:
        print(f"An exception was thrown: {error}\nStackTrace: {traceback.format_exc()}")
        sys.exit(1)
