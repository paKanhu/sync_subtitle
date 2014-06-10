"""
A collection of functions to synchronize subtitle (SRT) file

Synchronizes i.e. delays, or hastens a complete subtitle (SRT) file, or
part of it

Functions:

sync                         -- Synchronizes a complete subtitle file
sync_after_time              -- Synchronizes the subtitles occuring after a
                                specified time
sync_before_time             -- Synchronizes the subtitles occuring before a
                                specified time
sync_between_times           -- Synchronizes the subtitles occuring between the
                                specified starting and ending times
sync_after_index             -- Synchronizes the subtitles occuring after a
                                specified index
sync_before_index            -- Synchronizes the subtitles occuring before a
                                specified index
sync_between_indexes         -- Synchronizes the subtitles occuring between the
                                specified starting and ending indexes
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

__all__ = ['sync', 'sync_after_time', 'sync_before_time', 'sync_between_times',\
            'sync_after_index', 'sync_before_index', 'sync_between_indexes']
SUBTITLE_INDEX_FLAG = True

def sync(input_file, sync_time_in_ms, delay=True, output_file=''):
    """
    Synchronizes a complete subtitle file.

        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will be
                                delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file
        try:
            with open(input_file) as inputfile:
                with open(output_file + '.tmp', 'w') as outputfile:
                    for each_line in inputfile:

                        (start_time, end_time) = \
                            get_start_and_end_times(each_line)

                        if (start_time != None) or (end_time != None):

                            (start_time, end_time) = get_sync_times(\
                                sync_time_in_ms, start_time, end_time, delay)

                            print(ms_to_str(start_time) + ' --> ' + \
                                ms_to_str(end_time), file=outputfile)

                        else:
                            print(each_line, end='', file=outputfile)
            save_srt_file(input_file, output_file)
        except IOError as ioerr:
            print('File error: ' + str(ioerr))



def sync_after_time(sync_after_time_str, input_file, sync_time_in_ms, \
    delay=True, output_file=''):
    """
    Synchronizes the subtitles occuring after a specified time.

        sync_after_time_str  -- Time after which synchronization will start.
                                It is a string in the format of hh:mm:ss,ms
                                (01:23:45,678).
        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will be
                                delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file
        if check_time_str_format(sync_after_time_str):
            try:
                with open(input_file) as inputfile:
                    with open(output_file + '.tmp', 'w') as outputfile:
                        for each_line in inputfile:

                            sync_after_time_in_ms = \
                                str_to_ms(sync_after_time_str)

                            (start_time, end_time) = \
                                get_start_and_end_times(each_line)

                            if (start_time != None) or (end_time != None):
                                if sync_after_time_in_ms < start_time:

                                    (start_time, end_time) = \
                                        get_sync_times(sync_time_in_ms, \
                                            start_time, end_time, delay)

                                    print(ms_to_str(start_time) + ' --> ' + \
                                        ms_to_str(end_time), file=outputfile)

                                else:
                                    print(each_line, end='', file=outputfile)
                            else:
                                print(each_line, end='', file=outputfile)
                save_srt_file(input_file, output_file)
            except IOError as ioerr:
                print('File error: ' + str(ioerr))



def sync_before_time(sync_before_time_str, input_file, sync_time_in_ms, \
    delay=True, output_file=''):
    """
    Synchronizes the subtitles occuring before a specified time.

        sync_before_time_str -- Time before which synchronization will be done.
                                It is a string in the format of hh:mm:ss,ms
                                (01:23:45,678).
        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will
                                be delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file
        if check_time_str_format(sync_before_time_str):
            try:
                with open(input_file) as inputfile:
                    with open(output_file + '.tmp', 'w') as outputfile:
                        for each_line in inputfile:

                            sync_before_time_in_ms = \
                                str_to_ms(sync_before_time_str)

                            (start_time, end_time) = \
                                get_start_and_end_times(each_line)

                            if (start_time != None) or (end_time != None):
                                if sync_before_time_in_ms > end_time:

                                    (start_time, end_time) = \
                                        get_sync_times(sync_time_in_ms, \
                                            start_time, end_time, delay)

                                    print(ms_to_str(start_time) + ' --> ' + \
                                        ms_to_str(end_time), file=outputfile)

                                else:
                                    print(each_line, end='', file=outputfile)
                            else:
                                print(each_line, end='', file=outputfile)
                save_srt_file(input_file, output_file)
            except IOError as ioerr:
                print('File error: ' + str(ioerr))



def sync_between_times(sync_after_time_str, sync_before_time_str, input_file, \
    sync_time_in_ms, delay=True, output_file=''):
    """
    Synchronizes the subtitles occuring between the specified starting and
    ending times.

        sync_after_time_str  -- Time after which synchronization will start.
                                It is a string in the format of hh:mm:ss,ms
                                (01:23:45,678).
        sync_before_time_str -- Time before which synchronization will be done.
                                It is a string in the format of hh:mm:ss,ms
                                (01:23:45,678).
        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will
                                be delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file

        if check_time_str_format(sync_after_time_str) and \
            check_time_str_format(sync_before_time_str):

            try:
                with open(input_file) as inputfile:
                    with open(output_file + '.tmp', 'w') as outputfile:
                        for each_line in inputfile:

                            sync_after_time_in_ms = \
                                str_to_ms(sync_after_time_str)

                            sync_before_time_in_ms = \
                                str_to_ms(sync_before_time_str)

                            (start_time, end_time) = \
                                get_start_and_end_times(each_line)

                            if (start_time != None) or (end_time != None):

                                if (sync_after_time_in_ms < start_time) and \
                                    (sync_before_time_in_ms > end_time):

                                    (start_time, end_time) = \
                                        get_sync_times(sync_time_in_ms, \
                                            start_time, end_time, delay)

                                    print(ms_to_str(start_time) + ' --> ' + \
                                        ms_to_str(end_time), file=outputfile)

                                else:
                                    print(each_line, end='', file=outputfile)
                            else:
                                print(each_line, end='', file=outputfile)
                save_srt_file(input_file, output_file)
            except IOError as ioerr:
                print('File error: ' + str(ioerr))



def sync_after_index(index, input_file, sync_time_in_ms, delay=True, \
    output_file=''):
    """
    Synchronizes the subtitles occuring after a specified index.

        index                -- Index after which synchronization will be done.
                                If index < 1, this function will be same as
                                sync().
        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will
                                be delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file
        try:
            with open(input_file) as inputfile:
                with open(output_file + '.tmp', 'w') as outputfile:
                    subtitle_index = 0
                    for each_line in inputfile:
                        if is_index(each_line):
                            subtitle_index = int(each_line)
                        if subtitle_index > index:

                            (start_time, end_time) = \
                                get_start_and_end_times(each_line)

                            if (start_time != None) or (end_time != None):

                                (start_time, end_time) = \
                                    get_sync_times(sync_time_in_ms, start_time,\
                                        end_time, delay)

                                print(ms_to_str(start_time) + ' --> ' + \
                                    ms_to_str(end_time), file=outputfile)

                            else:
                                print(each_line, end='', file=outputfile)
                        else:
                            print(each_line, end='', file=outputfile)
            save_srt_file(input_file, output_file)
        except IOError as ioerr:
            print('File error: ' + str(ioerr))



def sync_before_index(index, input_file, sync_time_in_ms, delay=True, \
    output_file=''):
    """
    Synchronizes the subtitles occuring before a specified index.

        index                -- Index before which synchronization will be done.
        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will
                                be delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file
        try:
            with open(input_file) as inputfile:
                with open(output_file + '.tmp', 'w') as outputfile:
                    subtitle_index = 0
                    for each_line in inputfile:
                        if is_index(each_line):
                            subtitle_index = int(each_line)
                        if subtitle_index < index:

                            (start_time, end_time) = \
                                get_start_and_end_times(each_line)

                            if (start_time != None) or (end_time != None):

                                (start_time, end_time) = \
                                    get_sync_times(sync_time_in_ms, start_time,\
                                        end_time, delay)

                                print(ms_to_str(start_time) + ' --> ' + \
                                    ms_to_str(end_time), file=outputfile)

                            else:
                                print(each_line, end='', file=outputfile)
                        else:
                            print(each_line, end='', file=outputfile)
            save_srt_file(input_file, output_file)
        except IOError as ioerr:
            print('File error: ' + str(ioerr))



def sync_between_indexes(start_index, end_index, input_file, sync_time_in_ms, \
    delay=True, output_file=''):
    """
    Synchronizes the subtitles occuring between the specified starting and
    ending times.

        start_index          -- Index after which synchronization will be done.
        end_index            -- Index before which synchronization will be done.
        input_file           -- Path to the input SRT file.
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will
                                be delayed, or hastened.
        delay                -- True for delaying the subtitle, False for
                                hastening it.
        output_file          -- With default value input file will be replaced.
                                Change it to get output in different file.
    """

    if check_srt_extension(input_file):
        if output_file == '':
            output_file = input_file
        try:
            with open(input_file) as inputfile:
                with open(output_file + '.tmp', 'w') as outputfile:
                    subtitle_index = 0
                    for each_line in inputfile:
                        if is_index(each_line):
                            subtitle_index = int(each_line)

                        if (subtitle_index > start_index) and (subtitle_index <\
                            end_index):

                            (start_time, end_time) = \
                                get_start_and_end_times(each_line)

                            if (start_time != None) or (end_time != None):

                                (start_time, end_time) = \
                                    get_sync_times(sync_time_in_ms, start_time,\
                                        end_time, delay)

                                print(ms_to_str(start_time) + ' --> ' + \
                                    ms_to_str(end_time), file=outputfile)

                            else:
                                print(each_line, end='', file=outputfile)
                        else:
                            print(each_line, end='', file=outputfile)
            save_srt_file(input_file, output_file)
        except IOError as ioerr:
            print('File error: ' + str(ioerr))



def get_start_and_end_times(input_line):
    """
    Returns the start annd end time of a subtile line if the 'input_line'
    matches hh:mm:ss,ms --> hh:mm:ss,ms format, otherwise retuns 'None' for
    both start and end time.

        input_line           -- String to be check against time pattern to get
                                start and end time
    """

    is_time_str = \
        re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', \
            input_line)

    if is_time_str != None:
        (start_time_str, end_time_str) = input_line.split(' --> ')
        start_time = str_to_ms(start_time_str)
        end_time = str_to_ms(end_time_str)
    else:
        start_time = None
        end_time = None
    return (start_time, end_time)



def get_sync_times(sync_time_in_ms, start_time, end_time, delay):
    """
        sync_time_in_ms      -- Time (in millisecond) for which subtitle will
                                be delayed, or hastened.
        start_time           -- Subtitle line start time (in millisecond)
        end_time             -- Subtitle line end time (in millisecond)
        delay                -- True for delaying the subtitle, False for
                                hastening it.
    """

    if delay:
        start_time += sync_time_in_ms
        end_time += sync_time_in_ms
    else:
        if start_time > sync_time_in_ms:    # To prevent negative start time
            start_time -= sync_time_in_ms
        if (end_time - sync_time_in_ms) > start_time: # To prevent end time
                                                      # smaller than start time
            end_time -= sync_time_in_ms
    return (start_time, end_time)



def save_srt_file(input_file, output_file):
    """
        input_file           -- Input subtitle file
        output_file          -- Output subtitle file
    """
    if input_file == output_file:
        try:
            os.remove(input_file)
        except NotImplementedError as nierr:
            print('File modification error: ' + str(nierr))
    try:
        os.rename(output_file + '.tmp', output_file)
    except NotImplementedError as nierr:
        print('File modification error: ' + str(nierr))



def str_to_ms(time_str):
    """
        time_str             -- Time string in (hh:mm:ss,ms) format
    """
    (hhmmss_str, ms_str) = time_str.split(',')
    (hh_str, mm_str, ss_str) = hhmmss_str.split(':')

    return ((int(hh_str) * 3600) + (int(mm_str) * 60) + int(ss_str)) * 1000 + \
        int(ms_str)



def ms_to_str(time_in_ms):
    """
        time_in_ms           -- Time in millisecond
    """
    hour = int(time_in_ms / 3600000)
    time_in_ms = time_in_ms % 3600000

    minute, second, millisecond = int(time_in_ms / 60000), \
        int(time_in_ms % 60000 / 1000), time_in_ms % 1000

    return '{:0=2}:{:0=2}:{:0=2},{:0=3}'.format(hour, minute, second, \
        millisecond)



def check_srt_extension(input_file):
    """
        input_file           -- Input file to be checked for .srt extension
    """
    if input_file.endswith('.srt'):
        return True
    else:
        print('Error: File needs to have .srt extension. Check the input file.')
        return False



def check_time_str_format(time_str):
    """
        time_str             -- Time string in (hh:mm:ss,ms) format
    """
    is_time_str = re.match(r'\d{2}:\d{2}:\d{2},\d{3}', time_str)
    if is_time_str != None:
        return True
    else:
        print('Error: Time string must be in the format of hh:mm:ss,ms' + \
            '(01:23:45,678).')
        return False



def is_index(input_line):
    """
        input_line           -- String to be check against time pattern to get
                                start and end time
    """
    global SUBTITLE_INDEX_FLAG
    if SUBTITLE_INDEX_FLAG:
        isindex = re.match(r'^[\d]+$', input_line)
        if isindex:
            SUBTITLE_INDEX_FLAG = False
            return True
    else:
        isnewline = re.match(r'^\n', input_line)
        if isnewline:
            SUBTITLE_INDEX_FLAG = True
    return False
