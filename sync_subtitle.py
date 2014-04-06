"""
sync_subtitle

Synchronizes i.e. delays, or hastens a subtitle (SRT) file

Copyright (C) 2014 Prasannajit Acharya - Kanhu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import os
import re

"""This is "sync_subtitle.py" module and it provides sync_subtitle() function,
which synchronizes a subtitle file i.e. delays, or hastens the subtitle.
Note: Only applicable to SRT file."""

def sync_subtitle(srt_file, sync_time_in_ms , delay = True, inplace = False):
    """"srt_file" is a string, which is the name of the input SRT file.
       "sync_time_in_ms" is the time (in millisecond) for which subtitle will be
       delayed, or hastened. "delay" argument is used to define if the subtitle
       will be delayed, or hastened. Default for "delay" is True. "inplace"
       argument is used to define if in-place change will occur to the input
       file for "inplace" value True, or a new subtitle file will be created
       with name "sync_subtitle.srt". Default value of inplace is False."""
    try:
        with open(srt_file) as input_file:
            with open('sync_subtitle.srt', 'w') as output_file:
                for each_line in input_file:
                    is_time_str = re.match(r'\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d', each_line)
                    if is_time_str != None:
                        (start_time_str, end_time_str) = each_line.split(' --> ')
                        start_time = str_to_ms(start_time_str)
                        end_time = str_to_ms(end_time_str)
                        if delay:
                            if start_time > sync_time_in_ms:
                                start_time -= sync_time_in_ms
                            if (end_time - sync_time_in_ms) > start_time:
                                end_time -= sync_time_in_ms
                        else:
                            start_time += sync_time_in_ms
                            end_time += sync_time_in_ms
                        print(ms_to_str(start_time) + ' --> ' + ms_to_str(end_time), file=output_file)
                    else:
                        print(each_line, end='', file=output_file)
    except IOError as ioerr:
        print('File error: ' + str(ioerr))

    if inplace:
        try:
            os.remove(srt_file)
            os.rename('sync_subtitle.srt', srt_file)
        except NotImplementedError as nierr:
            print('File modification error: ' + str(nierr))

def str_to_ms(time_str):
    (hhmmss_str, ms_str) = time_str.split(',')
    (hh_str, mm_str, ss_str) = hhmmss_str.split(':')
    return(((int(hh_str) * 3600) + (int(mm_str) * 60) + int(ss_str)) * 1000 + int(ms_str))

def ms_to_str(time_in_ms):
    hh = int(time_in_ms / 3600000)
    time_in_ms = time_in_ms % 3600000
    mm , ss, ms = int(time_in_ms / 60000) , int(time_in_ms % 60000 / 1000), time_in_ms % 1000
    return('{:0=2}:{:0=2}:{:0=2},{:0=3}'.format(hh, mm, ss, ms))

