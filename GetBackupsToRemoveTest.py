#!/usr/bin/env python3
import unittest
import BackupAutoRemove

class GetBackupsToRemoveTest(unittest.TestCase):

    def test_remove_one(self):
        max_backups = 5
        files = ["backup-2021-06-11", "backup-2021-06-12", "backup-2021-06-13", "backup-2021-06-14", "backup-2021-06-15"]
        backups_to_remove = BackupAutoRemove.get_backups_to_remove(10, )
        self.assertEqual("", base64.ascii_to_base64(""))


if __name__ == "__main__":
    unittest.main()
