Subtitle (SRT) Synchronizer
---------------------------

Synchronizes a .srt subtitle file.
    - Takes time in millisecond
    - Option for delaying and hastening
    - Option for in-place modification
    - Does not make change any change, if ending time of subtitle file is
      smaller than starting time, which occurs when delaying more than the
      starting time of the subtitle. It generally occurs for first subtitle.

This version requires Python 3 or later.
