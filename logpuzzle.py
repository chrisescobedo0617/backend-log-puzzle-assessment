#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    url_list = []
    list_ = []
    with open(filename) as f:
        log_file = f.read()
    url_pattern = re.compile(r'GET (\S+.jpg) HTTP')
    server_pattern = re.compile(r'_(\S+)')
    server_match = server_pattern.finditer(filename)
    matches = url_pattern.finditer(log_file)
    for s_match in server_match:
        for match in matches:
            url = f"http://{s_match.group(1)}{match.group(1)}"
            if url not in url_list:
                url_list.append(url)
    sorted_url_list = sorted(url_list)
    for url in sorted_url_list:
        list_.append(url.split('-'))
    sorted_list = sorted(list_,key=lambda url: url[-1])
    list_of_strings = ['-'.join(url)for url in sorted_list]
    list_of_strings.pop()
    if 'animal_code' in filename:
        return sorted_url_list
    return list_of_strings


def image_src(url_list):
    string = ''
    for num, url in enumerate(url_list):
        string += f'<img src="img{num}">'
    return string


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    else:
        print('sorry, path exists')
    os.chdir(dest_dir)
    for num, image in enumerate(img_urls):
        print(f'Retrieving ... {image}')
        file_name = f'img{num}'
        urllib.request.urlretrieve(image, file_name)
    with open('index.html','w') as f:
        message = f"""<html>
        <body>{image_src(img_urls)}</body>
        </html>
        """
        f.write(message)

def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
