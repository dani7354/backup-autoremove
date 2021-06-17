#!/usr/bin/env python3
from time import strptime
import unittest
import BackupAutoRemove

class GetBackupsToRemoveTest(unittest.TestCase):

    def test_remove_one(self):
        max_backups = 3
        date_format = "%Y-%m-%d"
        files = [(strptime("2021-01-16", date_format), "backup-2021-01-16"),(strptime("2021-10-10", date_format), "backup-2021-10-10"), (strptime("2020-09-30", date_format),"backup-2020-09-30"),  (strptime("2020-10-30", date_format),"backup-2020-10-30")] 
        backups = BackupAutoRemove.get_backups_to_remove(files, max_backups)
        self.assertEqual("backup-2020-09-30", backups[0])
    
    def test_remove_two(self):
        max_backups = 3
        date_format = "%Y-%m-%d"
        files = [(strptime("2021-01-16", date_format), "backup-2021-01-16"), (strptime("2021-10-10", date_format), "backup-2021-10-10"), (strptime("2020-09-30", date_format),"backup-2020-09-30"), (strptime("2021-12-12", date_format), "backup-2021-12-12"), (strptime("2020-10-30", date_format),"backup-2020-10-30")] 
        backups = BackupAutoRemove.get_backups_to_remove(files, max_backups)
        self.assertEqual("backup-2020-09-30", backups[0])
        self.assertEqual("backup-2020-10-30", backups[1])
    
    def test_remove_none(self):
        max_backups = 3
        date_format = "%Y-%m-%d"
        files = [(strptime("2020-09-30", date_format),"backup-2020-09-30"),  (strptime("2020-10-30", date_format),"backup-2020-10-30")]
        backups = BackupAutoRemove.get_backups_to_remove(files, max_backups)
        self.assertEqual(0, len(backups))

    def test_remove_no_files(self):
        max_backups = 3
        files = []
        backups = BackupAutoRemove.get_backups_to_remove(files, max_backups)
        self.assertEqual(0, len(backups))
    
    def test_remove_files_is_none(self):
        max_backups = 3
        files = None
        backups = BackupAutoRemove.get_backups_to_remove(files, max_backups)
        self.assertEqual(0, len(backups))

    def test_backup_count_zero(self):
        max_backups = 0
        date_format = "%Y-%m-%d"
        files = [(strptime("2021-01-16", date_format), "backup-2021-01-16"),(strptime("2021-10-10", date_format), "backup-2021-10-10"), (strptime("2020-09-30", date_format),"backup-2020-09-30"),  (strptime("2020-10-30", date_format),"backup-2020-10-30")] 
        backups = BackupAutoRemove.get_backups_to_remove(files, max_backups)
        self.assertEqual(len(files), len(backups))
    
    def test_backup_count_negative(self):
        max_backups = -99
        date_format = "%Y-%m-%d"
        files = [(strptime("2021-01-16", date_format), "backup-2021-01-16"),(strptime("2021-10-10", date_format), "backup-2021-10-10"), (strptime("2020-09-30", date_format),"backup-2020-09-30"),  (strptime("2020-10-30", date_format),"backup-2020-10-30")] 
        with self.assertRaises(ValueError):
            BackupAutoRemove.get_backups_to_remove(files, max_backups)

if __name__ == "__main__":
    unittest.main()
