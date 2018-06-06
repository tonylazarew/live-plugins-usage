# Why?

I decided to write this script just for fun when a friend asked me, what's my top-5 plugins and I couldn't answer :-)

There might already be something similar, too lazy to check.

# How to use?

Just grab the `analyze-live-plugins.py` and run it with `--help`, it'll explain everything.

```
$ python analyze-live-plugins.py --help
usage: analyze-live-plugins.py [-h] [-o OUTPUT_CSV] ROOT

This script walks through whatever root folder you pass it, finds all Live
projects in there and aggregates the plugins usage info. Known to work with
Live 9 and 10 projects.

positional arguments:
  ROOT                  Root folder with Ableton Live projects to scan through

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_CSV, --output OUTPUT_CSV
                        Output CSV file path (default: prints to stdout)

```

It will write a CSV data out either to a file (if you provide `-o` flag) or to the stdout (terminal or pipe).

Use that data to know your habits! ;-)

# Does it work with Live 10?

Yes. I tested it against both Live 9 and 10 projects. No idea about earlier versions, don't have any projects around.
