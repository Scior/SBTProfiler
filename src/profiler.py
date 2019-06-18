#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import cProfile
import gzip
import pstats
import re
import time
from operator import itemgetter

def read_activity_log(path):
    """
    Reads the `xcactivitylog` file from the given path and unzip it.
    Args:
        - path: Path to the `xcactivitylog` file.
    Returns:
        [(float, string)]: List of the tuple of consumpted time and description. 
    """

    start = time.time()
    with gzip.open(args.file, mode='rt') as file:
        prog = re.compile('^\d+\.\d+ms')
        profiles = set()
        for item in file.read().split('\n'):
            if prog.match(item):
                items = item.split('\t', 1)
                profiles.add((float(items[0].strip('ms')), items[1]))

    return list(profiles)


def print_profile_summary(profiles, count=20):
    """
    Prints the summary of the profile.
    Args:
        - profiles: Profile to print.
        - count: Count of methods to show in the summary.
    """

    total_time = sum([profile[0] for profile in profiles])
    print('Rate\tTime\tMethod Name')
    print('-------------------------------')
    for line in sorted(profiles, key=itemgetter(0), reverse=True)[0:count]:
        rate = 100.0 * line[0] / total_time
        print('%.2f%%\t' % rate + '%.2fms\t%s' % line)
    
    print('-------------------------------')
    print('Total Time: %.2fs' % (total_time / 1000.0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Profile the time for building iOS sources')
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode')
    parser.add_argument('file', help='file to analyze')
    args = parser.parse_args()

    if args.debug:
        profile = cProfile.Profile()
        profile.enable()

    profiles = read_activity_log(args.file)
    print_profile_summary(profiles)

    if args.debug:
        stats = pstats.Stats(profile)
        profile.disable()
        stats.sort_stats('tottime')
        stats.print_stats()
