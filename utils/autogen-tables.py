#!/usr/bin/env python3

"""
Autogenerate tables from filenames

Script to generate markdown tables from filenames in a given folder. This script is specific to this project in that the filenames are parsed with decimals as delimiters.

[module].[section].[resource].resource-name.[attribution].[extention]

Example call:
python autogen-tables.py -d [path/to/directory]

License: Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0)
"""

import argparse
import os
import re

# Authorship
__author__ = "Shawn Hymel"
__copyright__ = "Copyright 2022, Edge Impulse"
__license__ = "Apache 2.0"
__version__ = "1.0"

################################################################################
# Settings

absolute_paths = False      # True to append repo_url to every link
repo_url = "https://github.com/edgeimpulse/courseware-embedded-machine-learning/"
colab_url = "https://colab.research.google.com/github/edgeimpulse/courseware-embedded-machine-learning/blob/main/"
raw_url = "raw/main/"
raw_append = "?raw=true"
attr_urls = [
    "#1-slides-and-written-material-for-introduction-to-embedded-machine-learning-by-edge-impulse-is-licensed-under-cc-by-nc-sa-40",
    "#2-slides-and-written-material-for-computer-vision-with-embedded-machine-learning-by-edge-impulse-is-licensed-under-cc-by-nc-sa-40",
    "#3-slides-and-written-material-for-tinyml-courseware-by-tinymlx-is-licensed-under-cc-by-nc-sa-40"
]

################################################################################
# Functions

################################################################################
# Main

# Script arguments
parser = argparse.ArgumentParser(description="Script that looks through "
            "filenames in given directory and auto-generates markdown "
            "tables and links")
group = parser.add_mutually_exclusive_group()
group.add_argument('-d',
                   '--directory',
                   action='store',
                   dest='dir_path',
                   type=str,
                   help="Directory containing the files you want to list in "
                        "the table.")
group.add_argument('directory', nargs='?')

# Parse the arguments
args = parser.parse_args()
dir_path = ""
if args.dir_path:
    dir_path = args.dir_path
elif args.directory:
    dir_path = args.directory
else:
    print("ERROR: no directory given")
    exit()

# Get files in directory (ignore subdirectories)
filenames = []
for f in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, f)):
        filenames.append(f)

# Split filenames and sort based on ID number
filenames_split = [f.split('.') for f in filenames]
filenames_split.sort(key=lambda x: (int(x[0]), int(x[1]), int(x[2])))

# Go through files
for parsed in filenames_split:

    # Get ID and description
    id = str(parsed[0]) + "." + str(parsed[1]) + "." + str(parsed[2])
    desc = parsed[3].replace('-', ' ').capitalize()
    
    # Construct link based on file type
    f = '.'.join(parsed)
    link = dir_path + '/' + f
    if parsed[5] == 'docx':
        if absolute_paths:
            link = repo_url + raw_url + link
        else:
            link = link + raw_append
        link = link.replace(' ', '%20')
        link = "[doc](" + link + ")"
    elif parsed[5] == 'pptx':
        if absolute_paths:
            link = repo_url + raw_url + link
        else:
            link = link + raw_append
        link = link.replace(' ', '%20')
        link = "[slides](" + link + ")"
    elif parsed[5] == 'ipynb':
        link = colab_url + link
        link = link.replace(' ', '%20')
        link = "[colab](" + link + ")"
    else:
        print("ERROR: Unsupported file type: " + f)
        exit()
    
    # Create attribution link
    attr = parsed[4]
    if not attr.isnumeric():
        print("ERROR: Attribution must be a number: " + f)
        exit()
    attr = int(attr)
    if (attr > 0) and (attr <= len(attr_urls)):
        attr_url = ""
        if absolute_paths:
            attr_url = repo_url
        attr_url = attr_url + attr_urls[attr - 1]
        attr = "[[" + str(attr) + "]](" + attr_url + ")"
    else:
        attr = ""
    
    # Print table entry
    print("| " + id + " | " + desc + " | " + link + " | " + attr + " |")