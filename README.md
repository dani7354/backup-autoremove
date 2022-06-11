# backup-autoremove
A Python script for removing old backups inside a folder keeping only the x newest backups. The script is intended to be
run as a cron job.

## Usage from terminal
After having download the script, it can be run manually like this (but I suggest that you set it up as a cronjob)
```
$ ./backup-auto-remove.py -l "/path/to/dir/containing/backups" -d "\%Y\%m\%d" -p "[0-9]{8}" -m 90
```

### Arguments explained:
* __-l or --location__: Directory containing the backups (required).
* __-d or --date-format__: Date format (required). The date format specified in this example will match dates in this format: 20211201.
* __-p or --regex-pattern__: Regex pattern for recognizing the date in the file or folder names, so the script will know which part to parse as a date (required).
* __-m or --max-backup-count__: Max backups to keep (required). In this example the 90 most recent backups will be kept.
