"""
A collection of functions to synchronize subtitle (SRT) file

Synchronizes i.e. delays, or hastens a complete subtitle (SRT) file, or
part of it

Functions:

sync               -- Synchronizes a complete subtitle file
sync_after_time    -- Synchronizes the subtitles occuring after a
                      specified time
sync_before_time   -- Synchronizes the subtitles occuring before a
                      specified time
sync_between_times -- Synchronizes the subtitles occuring between the
                      specified starting and ending times
"""

"""
The MIT License (MIT)

Copyright (c) 2014 Prasannajit Acharya - Kanhu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import os
import re

__all__ = ['sync', 'sync_after_time', 'sync_before_time', 'sync_between_times']

def sync(input_srt_file, sync_time_in_ms , delay = True, output_srt_file = ''):
    """
		input_srt_file      -- Path to the input SRT file.
		sync_time_in_ms     -- Time (in millisecond) for which subtitle will be
		                       delayed, or hastened.
		delay               -- True for delaying the subtitle, False for
		                       hastening it.
		output_srt_file     -- With default value input file will be replaced.
		                       Change it to get output in different file.
    """
    if check_srt_extension(input_srt_file):
        if output_srt_file == '':
            output_srt_file = input_srt_file
        try:
            with open(input_srt_file) as input_file:
                with open(output_srt_file + '.tmp', 'w') as output_file:
                    for each_line in input_file:
                        (start_time, end_time) = get_start_and_end_times(each_line)
                        if (start_time != None) or (end_time != None):
                            (start_time, end_time) = get_sync_times(sync_time_in_ms, start_time, end_time, delay)
                            print(ms_to_str(start_time) + ' --> ' + ms_to_str(end_time), file=output_file)
                        else:
                            print(each_line, end='', file=output_file)
            save_srt_file(input_srt_file, output_srt_file)
        except IOError as ioerr:
            print('File error: ' + str(ioerr))



def sync_after_time(sync_after_time_str, input_srt_file, sync_time_in_ms , delay = True, output_srt_file = ''):
    """
		sync_after_time_str -- Time after which synchronization will start.
		                       It is a string in the format of hh:mm:ss,ms
		                       (01:23:45,678).
		input_srt_file      -- Path to the input SRT file.
		sync_time_in_ms     -- Time (in millisecond) for which subtitle will be
		                       delayed, or hastened.
		delay               -- True for delaying the subtitle, False for
		                       hastening it.
		output_srt_file     -- With default value input file will be replaced.
		                       Change it to get output in different file.
    """
    if check_srt_extension(input_srt_file):
        if output_srt_file == '':
            output_srt_file = input_srt_file
        if check_time_str_format(sync_after_time_str):
            try:
                with open(input_srt_file) as input_file:
                    with open(output_srt_file + '.tmp', 'w') as output_file:
                        for each_line in input_file:
                            sync_after_time = str_to_ms(sync_after_time_str)
                            (start_time, end_time) = get_start_and_end_times(each_line)
                            if (start_time != None) or (end_time != None):
                                if sync_after_time < start_time:
                                    (start_time, end_time) = get_sync_times(sync_time_in_ms, start_time, end_time, delay)
                                    print(ms_to_str(start_time) + ' --> ' + ms_to_str(end_time), file=output_file)
                                else:
                                    print(each_line, end='', file=output_file)
                            else:
                                print(each_line, end='', file=output_file)
                save_srt_file(input_srt_file, output_srt_file)
            except IOError as ioerr:
                print('File error: ' + str(ioerr))



def sync_before_time(sync_before_time_str, input_srt_file, sync_time_in_ms , delay = True, output_srt_file = ''):
    """
		sync_before_time_str -- Time before which synchronization will be done.
		                        It is a string in the format of hh:mm:ss,ms
		                        (01:23:45,678).
		input_srt_file       -- Path to the input SRT file.
		sync_time_in_ms      -- Time (in millisecond) for which subtitle will
		                        be delayed, or hastened.
		delay                -- True for delaying the subtitle, False for
		                        hastening it.
		output_srt_file      -- With default value input file will be replaced.
		                        Change it to get output in different file.
    """
    if check_srt_extension(input_srt_file):
        if output_srt_file == '':
            output_srt_file = input_srt_file
        if check_time_str_format(sync_before_time_str):
            try:
                with open(input_srt_file) as input_file:
                    with open(output_srt_file + '.tmp', 'w') as output_file:
                        for each_line in input_file:
                            sync_before_time = str_to_ms(sync_before_time_str)
                            (start_time, end_time) = get_start_and_end_times(each_line)
                            if (start_time != None) or (end_time != None):
                                if sync_before_time > end_time:
                                    (start_time, end_time) = get_sync_times(sync_time_in_ms, start_time, end_time, delay)
                                    print(ms_to_str(start_time) + ' --> ' + ms_to_str(end_time), file=output_file)
                                else:
                                    print(each_line, end='', file=output_file)
                            else:
                                print(each_line, end='', file=output_file)
                save_srt_file(input_srt_file, output_srt_file)
            except IOError as ioerr:
                print('File error: ' + str(ioerr))



def sync_between_times(sync_after_time_str, sync_before_time_str, input_srt_file, sync_time_in_ms , delay = True, output_srt_file = ''):
    """
		sync_after_time_str  -- Time after which synchronization will start.
		                        It is a string in the format of hh:mm:ss,ms
		                        (01:23:45,678).
		sync_before_time_str -- Time before which synchronization will be done.
		                        It is a string in the format of hh:mm:ss,ms
		                        (01:23:45,678).
		input_srt_file       -- Path to the input SRT file.
		sync_time_in_ms      -- Time (in millisecond) for which subtitle will
		                        be delayed, or hastened.
		delay                -- True for delaying the subtitle, False for
		                        hastening it.
		output_srt_file      -- With default value input file will be replaced.
		                        Change it to get output in different file.
    """
    if check_srt_extension(input_srt_file):
        if output_srt_file == '':
            output_srt_file = input_srt_file
        if check_time_str_format(sync_after_time_str) and check_time_str_format(sync_before_time_str):
            try:
                with open(input_srt_file) as input_file:
                    with open(output_srt_file + '.tmp', 'w') as output_file:
                        for each_line in input_file:
                            sync_after_time = str_to_ms(sync_after_time_str)
                            sync_before_time = str_to_ms(sync_before_time_str)
                            (start_time, end_time) = get_start_and_end_times(each_line)
                            if (start_time != None) or (end_time != None):
                                if (sync_after_time < start_time) and (sync_before_time > end_time):
                                    (start_time, end_time) = get_sync_times(sync_time_in_ms, start_time, end_time, delay)
                                    print(ms_to_str(start_time) + ' --> ' + ms_to_str(end_time), file=output_file)
                                else:
                                    print(each_line, end='', file=output_file)
                            else:
                                print(each_line, end='', file=output_file)
                save_srt_file(input_srt_file, output_srt_file)
            except IOError as ioerr:
                print('File error: ' + str(ioerr))



def get_start_and_end_times(input_line):
    is_time_str = re.match(r'\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d', input_line)
    if is_time_str != None:
        (start_time_str, end_time_str) = input_line.split(' --> ')
        start_time = str_to_ms(start_time_str)
        end_time = str_to_ms(end_time_str)
    else:
        start_time = None
        end_time = None
    return (start_time, end_time)

def get_sync_times(sync_time_in_ms, start_time, end_time, delay):
    if delay:
        if start_time > sync_time_in_ms:
            start_time -= sync_time_in_ms
        if (end_time - sync_time_in_ms) > start_time:
            end_time -= sync_time_in_ms
    else:
        start_time += sync_time_in_ms
        end_time += sync_time_in_ms
    return (start_time, end_time)

def save_srt_file(input_srt_file, output_srt_file):
    if input_srt_file == output_srt_file:
        try:
            os.remove(input_srt_file)
        except NotImplementedError as nierr:
            print('File modification error: ' + str(nierr))
    try:
        os.rename(output_srt_file + '.tmp', output_srt_file)
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

def check_srt_extension(input_srt_file):
    if input_srt_file.endswith('.srt'):
        return True
    else:
        print('Error: File needs to have .srt extension. Check the input file.')
        return False

def check_time_str_format(time_str):
    is_time_str = re.match(r'\d\d:\d\d:\d\d,\d\d\d', time_str)
    if is_time_str != None:
        return True
    else:
        print('Error: Time string must be in the format of hh:mm:ss,ms (01:23:45,678).')
        return False

