#!/usr/bin/env python

'''This script walks through whatever root folder you pass it, finds all Live
projects in there and aggregates the plugins usage info.

Known to work with Live 9 and 10 projects.
'''

__author__ = 'Anton <code@lowkey.audio>'


import argparse
import gzip
import os
import re
import sys


rx_plugname = re.compile('<PlugName Value=\"([^\"]+)\" />')


def log_action(msg, verbose):
    if verbose:
        sys.stdout.write(msg + "\n")
        sys.stdout.flush()


def scan_als_file(als_path):
    plug_map = {}
    with gzip.open(als_path, 'rb') as fd:
        for line in fd:
            if 'PlugName' not in line:
                continue

            m = rx_plugname.search(line)
            if m is not None:
                plug_name = m.group(1)
                plug_map[plug_name] = plug_map.setdefault(plug_name, 0) + 1

    return plug_map


def merge_maps(map1, map2):
    ''' map1 <- map2 '''
    new_map = {}
    for key in sorted(set(map1.keys() + map2.keys())):
        new_map[key] = map1.get(key, 0) + map2.get(key, 0)

    return new_map


def scan_root(root, verbose=False):
    log_action('Scanning {0} ...'.format(root), verbose=verbose)

    global_plug_map = {}
    for r, dirs, files in os.walk(root):
        if 'Ableton Project Info' not in dirs:
            continue

        log_action(' - project folder: {0}'.format(r), verbose=verbose)

        for file_name in files:
            if '.als' not in file_name:
                continue

            als_path = os.path.join(r, file_name)

            log_action(' -- project file: {0}'.format(als_path), verbose=verbose)
            global_plug_map = merge_maps(
                global_plug_map,
                scan_als_file(als_path))

    return global_plug_map


def dump_csv(plug_map):
    '''Returns the CSV data ordered by most used to least used.
    '''
    csv_data = '"Plug-In Name","Usage Count"\n' + \
        '\n'.join(','.join(
            ('"{0}"'.format(k), str(v)))
            for k, v in sorted(plug_map.items(), key=lambda x: x[1], reverse=True))

    return csv_data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(metavar='ROOT', dest='root_folder',
        help='Root folder with Ableton Live projects to scan through')
    parser.add_argument('-o', '--output', metavar='OUTPUT_CSV',
        dest='output', default=None,
        help='Output CSV file path (default: prints to stdout)')
    args = parser.parse_args()

    verbose = False
    if args.output is None:
        output_fd = sys.stdout
    else:
        output_fd = open(args.output, 'w')
        verbose = True

    csv_data = dump_csv(scan_root(args.root_folder, verbose=verbose))
    output_fd.write(csv_data)

    if output_fd is not sys.stdout:
        output_fd.close()


if __name__ == '__main__':
    r = main()
    sys.exit(r)
