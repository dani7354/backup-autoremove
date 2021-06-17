#!/usr/bin/env python3
# dsp, 06-16-2021
from time import strptime
import re

DEFAULT_MAX_BACKUPS = 10

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

