# sync_subtitle's setup.py
from distutils.core import setup
setup(
    name = "sync_subtitle",
    version = "2.0.0",
    py_modules = ['sync_subtitle'],
    author = "Prasannajit Acharya - Kanhu",
    author_email = "prasannajit.acharya.kanhu@gmail.com",
    description = "Subtitle (SRT) synchronizer",
    keywords = ["subtitle", "srt", "synchronizer"],
    url = "https://github.com/paKanhu/sync_subtitle",
    license = "MIT License",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        ],
    long_description = """\
Subtitle (SRT) Synchronizer
---------------------------

Synchronizes i.e. delays, or hastens a .srt subtitle file.
    - Complete file synchronization
    - Synchronization before a specified time
    - Synchronization after a specified time
    - Synchronization between a time period

This version requires Python 3 or later.

"""
)
