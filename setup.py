# sync_subtitle's setup.py
from distutils.core import setup
setup(
    name = "sync_subtitle",
    version = "1.0.0",
    py_modules = ['sync_subtitle'],
    author = "Prasannajit Acharya - Kanhu",
    author_email = "prasannajit.acharya.kanhu@gmail.com",
    description = "Subtitle (SRT) synchronizer",
    keywords = ["subtitle", "srt", "synchronizer"],
    url = "https://github.com/paKanhu/sync_subtitle",
    license = "GNU General Public License v3 (GPLv3)",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        ],
    long_description = """\
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

"""
)
