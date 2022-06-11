#!/usr/bin/env python3
# 06-17-2021
# dsp 

from argparse import ArgumentParser
from time import strptime
import os
import re
import sys
import shutil
import traceback


def parse_date(regex_pattern, filename, date_format):
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


def location_is_valid(path):
    if not path is None:
        return os.path.isdir(path) and os.access(path, os.R_OK | os.W_OK)
    return False


if __name__ == "__main__":
    try:
        print("Starting autoremove...")

        parser = ArgumentParser(description="Deletes the oldest backups (files or folders) at the specified location",
                                add_help=False)
        parser.add_argument("-l", "--location", dest="location", type=str, required=True,
                            help="Folder containing the backup folders or files")
        parser.add_argument("-d", "--date-format", dest="date_format", type=str, required=True,
                            help="Format for parsing the date from the file or folder name (e.g. %Y-%m-%d)")
        parser.add_argument("-p", "--regex-pattern", dest="regex_pattern", type=str, required=True,
                            help="Regex pattern that matches the date in file or folder name")
        parser.add_argument("-m", "--backup-count", dest="max_backups", type=int, required=True,
                            help="Number of backups allowed at the specified location")
        arguments = vars(parser.parse_args())

        if not location_is_valid(arguments["location"]):
            raise ValueError(
                "Invalid value for argument for '-l, --location'. "
                "Check if the folder exists and the user has RW permissions!")

        print(f"Reading files at {arguments['location']}")
        files = os.listdir(arguments["location"])
        backups = []

        for file in files:
            try:
                backup_datetime = parse_date(arguments["regex_pattern"], file, arguments["date_format"])
                if backup_datetime is False:
                    continue
                print(f"Backup found: {file}")
                backups.append((backup_datetime, file))
            except ValueError:
                print(f"Error paring date from file: {file} - skipping to next!")
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
