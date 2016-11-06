#!/usr/bin/env python3.5

import argparse
import os
import shutil

from mod_xml2mongo import xml2mongo

parser = argparse.ArgumentParser(description='7z -> MongoDB')
parser.add_argument("file_path",help='''Please pass the following as argument
	7z file path (OR) directory path where xmls are located
	''')
args = parser.parse_args()

if os.path.isfile(args.file_path):
	xml2mongo(archive_path=args.file_path)
else:
	xml2mongo(xmls_dir=args.file_path)
