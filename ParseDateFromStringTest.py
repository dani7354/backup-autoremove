#!/usr/bin/env python3
from time import strptime
import unittest
import BackupAutoRemove


class GetBackupsToRemoveTest(unittest.TestCase):

    def test_parse_date_yyyy_mm_dd(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$" # Regular expression is simplified as the actual date validation takes place when calling the strptime() function
        file = "backup-2021-01-30"
        date_format = "%Y-%m-%d"
        backup_date = BackupAutoRemove.parse_date(regex_pattern, file, date_format)
        self.assertEqual(strptime("2021-01-30", date_format), backup_date)
    
    def test_parse_date_format_with_time(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}_[0-9]{2}_[0-9]{2}$" 
        file = "backup-2021-05-17T22_05_01"
        date_format = "%Y-%m-%dT%H_%M_%S"
        backup_date = BackupAutoRemove.parse_date(regex_pattern, file, date_format)
        self.assertEqual(strptime("2021-05-17T22_05_01", date_format), backup_date)

    def test_parse_date_no_separators(self):
        regex_pattern = "[0-9]{8}" 
        file = "backup-20210120.zip.enc"
        date_format = "%Y%m%d"
        backup_date = BackupAutoRemove.parse_date(regex_pattern, file, date_format)
        self.assertEqual(strptime("20210120", date_format), backup_date)

    def test_parse_date_empty_pattern(self):
        regex_pattern = ""
        file = "backup-2021-01-30"
        date_format = "%Y-%m-%d"
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)

    def test_parse_date_no_match(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        file = "someOtherfile.txt"
        date_format = "%Y-%m-%d"
        self.assertEqual(False, BackupAutoRemove.parse_date(regex_pattern, file, date_format))

    def test_parse_date_format_regex_differs(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        date_format = "%d-%m-%Y"
        file = "backup-2021-07-01"
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)

    def test_parse_date_empty_format(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        file = "backup-2021-01-30"
        date_format = ""
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)

    def test_parse_date_invalid_format(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        file = "backup-2021-01-30"
        date_format = "someString"
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)

    def test_parse_date_invalid_format_two(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        file = "backup-2021-01-30"
        date_format = "%Y-%d-%m"
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)

    def test_parse_date_empty_filename(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        file = ""
        date_format = "%Y-%m-%d"
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)
        
    def test_parse_date_format_none(self):
        regex_pattern = "[0-9]{4}-[0-9]{2}-[0-9]{2}$"
        file = "backup-2021-01-30"
        date_format = None
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)
     
    def test_parse_date_all_none(self):
        regex_pattern = None
        file = None
        date_format = None
        with self.assertRaises(ValueError):
            BackupAutoRemove.parse_date(regex_pattern, file, date_format)

if __name__ == "__main__":
    unittest.main()

